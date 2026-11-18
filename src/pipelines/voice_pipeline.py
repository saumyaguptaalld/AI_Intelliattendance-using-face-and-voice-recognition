from resemblyzer import VoiceEncoder, preprocess_wav  # resemblyzer converts speech to 256 D vector
                                                      # preprocess_wav prepares raw audio or numpy arrays so that they can be processed by VoiceEncoder
                                                      # resample, volume normalize, silence trimming, input format(accepts file path)
import numpy as np
import io
import librosa  # audio processing (instead of DL to extract speaker identity , it uses DSP to extract mathematical and structural features from audio)
import streamlit as st


@st.cache_resource
def load_voice_encoder():
    return VoiceEncoder()

def get_voice_embedding(audio_bytes):
    try:
        encoder = load_voice_encoder()

        # librosa returns audio and sample rate
        # audio given to desymblyzer for getting embedding
        audio, sr = librosa.load(io.BytesIO(audio_bytes), sr = 16000)

        # pre process audio by normalizinga nd silencing noise in audio
        wav = preprocess_wav(audio)
        embedding = encoder.embed_utterance(wav) # pre processed audio file used for obtaining embedding
        return embedding.tolist()  # 256D embedding is obtained
    except Exception as e:
        st.error(f"voice recognition error: {e}")
        return None

def identity_speaker(new_embedding, candidates_dict, threshold = 0.65):
    if new_embedding is None or not candidates_dict:
        return None, 0.0  # default similarity score of 0 and None means no speaker was identified
    best_sid = None
    best_score = -1.0
    new_embedding = np.asarray(new_embedding, dtype=np.float32)
    # Normalize new embedding
    new_norm = np.linalg.norm(new_embedding)
    if new_norm == 0:
        return None, 0.0
    new_embedding = new_embedding / new_norm
   
    for sid, stored_embedding in candidates_dict.items():  # student id and student embedding obtained from candidates dict
        if stored_embedding is None or len(stored_embedding) == 0:
            continue
        stored_embedding = np.asarray(stored_embedding, dtype=np.float32)
        if stored_embedding.shape != new_embedding.shape:
            continue
        stored_norm = np.linalg.norm(stored_embedding)
        if stored_norm == 0:
            continue
        stored_embedding = stored_embedding / stored_norm
        similarity = float(np.dot(new_embedding, stored_embedding))  # get similarity score with new embedding and stored embedding using the dot product
        if similarity > best_score:
            best_score = similarity
            best_sid = sid
    # After all candidates have been checked, decide whether the best match meets the threshold
    if best_score >= threshold:
        return best_sid, best_score
    
    return None, best_score

def process_bulk_audio(audio_bytes, candidates_dict, threshold = 0.65):
    try:
        encoder = load_voice_encoder()
        if not candidates_dict:
            st.warning("No enrolled students with voice embeddings found.")
            return {}
        audio, sr = librosa.load(io.BytesIO(audio_bytes),sr=16000)
        segments = librosa.effects.split(audio, top_db= 30)
        identified_speakers = {}
        for start,end in segments:
            if (end-start) > sr*0.5:  # sample rate should be good , and not whisper voices
                # obtain the segment audio
                segment_audio = audio[start:end]
                wav = preprocess_wav(segment_audio)
                embedding = encoder.embed_utterance(wav)

                sid, score = identity_speaker(embedding, candidates_dict, threshold)
                if sid is not None:
                    if (sid not in identified_speakers or score > identified_speakers[sid]):
                        identified_speakers[sid]= float(score)
        return identified_speakers
    except Exception as e:
        st.error(f"Bulk process error:{e}")
        return {}
    