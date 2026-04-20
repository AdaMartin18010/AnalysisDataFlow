# Real-Time Audio Stream Processing

> **Stage**: Knowledge/06-frontier/ | **Prerequisites**: [Multimodal Stream Processing Architecture](./multimodal-stream-processing.md) | **Formalization Level**: L3

---

## 1. Definitions

**Def-K-Audio-01: Real-Time Audio Stream Processing**
A stream computing application that performs real-time acquisition, feature extraction, event detection, classification recognition, and response triggering on continuous audio signals (e.g., speech, music, ambient sound). Typical scenarios include real-time speech transcription, music recommendation, abnormal sound detection, and voice assistant interaction.

**Def-K-Audio-02: Short-Time Fourier Transform (STFT)**
A method that divides time-domain audio signals into short frames and applies Fourier transform to each frame, yielding a time-frequency domain representation. STFT is one of the most fundamental feature extraction steps in audio stream processing.

**Def-K-Audio-03: Mel-Spectrogram**
A spectral representation designed based on human auditory characteristics, mapping the linear frequency axis to the Mel scale to better capture perceptually relevant information in speech and music.

---

## 2. Properties

**Lemma-K-Audio-01: Perceptual Boundary of Audio Stream Latency**
Human sensitivity to latency in voice interaction is approximately 200-300ms (conversational naturalness), while sensitivity to synchronization in music playback is approximately 20-40ms. Therefore, end-to-end latency for real-time speech processing systems should be < 200ms, and synchronization precision for multi-channel music mixing should be < 20ms.

**Lemma-K-Audio-02: Advantage of Decoupling Feature Extraction and Inference**
In audio stream processing, feature extraction such as Mel-spectrogram has low computational cost and latency, and can be executed at high frequency (e.g., every 10ms per frame); deep learning inference (e.g., speech recognition models) has high computational cost and is suitable for lower-frequency batch processing (e.g., every 500ms per batch). Decoupling the two can optimize resource utilization.

**Prop-K-Audio-01: Sliding Windows Are Key to Audio Event Detection**
Since audio events (e.g., keywords, abnormal sounds) can occur at any moment and have varying durations, using overlapping sliding windows can significantly improve event detection recall and prevent events from being missed when they cross window boundaries.

---

## 3. Relations

### 3.1 Audio Stream Processing Architecture

```mermaid
graph TB
    Mic[Microphone/Audio Source] --> Pre[Preprocessing<br/>Resampling/Denoising/VAD]
    Pre --> Feature[Feature Extraction<br/>STFT / Mel-Spectrogram / MFCC]
    Feature --> Flink[Flink Stream Processing<br/>Window Aggregation/Temporal Analysis]
    Flink --> Model[Model Inference<br/>ASR / Music Classification / Anomaly Detection]
    Model --> Output[Text/Events/Control Commands]
```

### 3.2 Comparison of Audio Processing with Other Modalities

| Characteristic | Audio Stream | Video Stream | Text Stream |
|----------------|--------------|--------------|-------------|
| Data Rate | Medium (16-128 kbps) | Extremely high (Mbps-Gbps) | Low (bps-kbps) |
| Typical Latency Requirement | < 200ms | < 1-3s | < 100ms |
| Core Features | Spectral/Temporal | Spatial/Temporal | Semantic/Syntactic |
| Inference Frequency | Medium (100-500ms) | Low (1-5s) | High (10-50ms) |
| Primary Hardware | CPU/GPU | GPU | CPU |

---

## 4. Argumentation

### 4.1 Core Challenges of Audio Stream Processing

1. **High Real-Time Requirements**: Speech recognition requires low latency to ensure conversational fluency.
2. **Complex Noise Environments**: Reverberation, background noise, and multiple simultaneous speakers in real-world scenes severely reduce recognition accuracy.
3. **Multilingual and Dialect Diversity**: With 7,000+ languages globally, mainstream ASR models still have limited support for low-resource languages.
4. **Privacy Sensitivity**: Voice data contains biometric information (voiceprints), creating strong demand for localized/edge processing.

### 4.2 Typical Application Scenarios

- **Real-Time Meeting Transcription**: Converting multi-person meeting speech to text in real time, supporting speaker diarization.
- **Intelligent Customer Service QA**: Real-time analysis of emotion, keywords, and compliance in customer service calls.
- **Industrial Anomaly Detection**: Monitoring equipment operation sounds via microphones to detect bearing wear, belt looseness, and other faults in advance.
- **Real-Time Music Recommendation**: Recommending the next song in real time based on the user's current music style and emotional state.

---

## 5. Proof / Engineering Argument

### 5.1 Completeness of Sliding Window Event Detection

**Theorem (Thm-K-Audio-01)**: Let the maximum duration of an audio event be $T_{max}$, the sliding window length be $W$, and the sliding step be $S$. If $W \geq T_{max}$ and $S \leq W / 2$, then any audio event will be covered by at least one complete window.

**Engineering Argument**:

1. Audio events are continuous in the time domain with length $t \leq T_{max}$.
2. Sliding windows advance with step $S$, and the uncovered gap between adjacent windows is $W - S$.
3. If $S \leq W / 2$, then $W - S \geq W / 2 > 0$, and any event of length $t \leq W$ cannot completely fall into the gap.
4. Therefore, every event will be fully captured by at least one window.
5. In practice, $W = 2 \times T_{max}$ and $S = W / 2$ are typically chosen to balance detection accuracy and computational overhead.

---

## 6. Examples

### 6.1 Flink Audio Feature Extraction Job

```java
// [Pseudocode snippet - not directly runnable] Core logic only
DataStream<AudioFrame> audioStream = env
    .addSource(new MicrophoneSource(16000, 1024))
    .assignTimestampsAndWatermarks(
        WatermarkStrategy.<AudioFrame>forBoundedOutOfOrderness(Duration.ofMillis(100))
    );

// 500ms sliding window, computing Mel-spectrogram
DataStream<MelSpectrogram> melStream = audioStream
    .windowAll(SlidingEventTimeWindows.of(Time.milliseconds(500), Time.milliseconds(250)))
    .process(new MelSpectrogramWindowFunction());

// Feed into ASR model
melStream
    .map(new AsrInferenceMapFunction())
    .addSink(new TranscriptSink());
```

### 6.2 Python Audio Feature Extraction UDF

```python
from pyflink.table.udf import udf
from pyflink.table import DataTypes
import librosa
import numpy as np

@udf(result_type=DataTypes.ARRAY(DataTypes.FLOAT()))
def extract_mel_features(audio_bytes, sample_rate=16000):
    y = np.frombuffer(audio_bytes, dtype=np.float32)
    mel_spec = librosa.feature.melspectrogram(y=y, sr=sample_rate, n_mels=128)
    log_mel = librosa.power_to_db(mel_spec, ref=np.max)
    return log_mel.flatten().tolist()
```

### 6.3 Voice Activity Detection (VAD) Configuration

```yaml
# WebRTC VAD configuration example vad:
  mode: 3  # 0=Normal, 1=LowBitRate, 2=Aggressive, 3=VeryAggressive
  frame_duration_ms: 30
  sample_rate: 16000
```

---

### 6.4 Challenges and Countermeasures in Audio Stream Processing

**Challenge 1: Robustness in Noisy Environments**

Industrial sites, public transportation, and open offices typically have SNR (Signal-to-Noise Ratio) below 10 dB, severely affecting ASR and event detection accuracy.

**Countermeasures**:

- **Signal Preprocessing**: Spectral subtraction, Wiener filtering to reduce stationary noise.
- **Neural Network Denoising**: Use lightweight models such as RNNoise and DeepFilterNet for real-time speech enhancement.
- **Multi-Channel Beamforming**: Microphone arrays leverage spatial information to enhance signals from the target direction.

```python
# Lightweight spectral subtraction denoising example
import numpy as np

def spectral_subtraction(signal, noise_estimate, alpha=1.5):
    """
    signal: time-domain audio frame
    noise_estimate: pre-estimated noise spectrum
    alpha: over-subtraction factor
    """
    spec = np.fft.rfft(signal)
    magnitude = np.abs(spec)
    phase = np.angle(spec)

    # Spectral subtraction + half-wave rectification
    cleaned_mag = np.maximum(magnitude - alpha * noise_estimate, 0.01 * magnitude)
    cleaned_spec = cleaned_mag * np.exp(1j * phase)

    return np.fft.irfft(cleaned_spec, n=len(signal))
```

**Challenge 2: Speaker Overlap (Cocktail Party Problem)**

Meeting scenarios often have multiple people speaking simultaneously, causing ASR to produce garbled transcription results.

**Countermeasures**:

- **Speaker Diarization**: Use clustering or end-to-end models (e.g., pyannote.audio) to identify "who spoke when."
- **Target Speaker Extraction**: Extract a specific speaker's voice based on an enrolled voiceprint.
- **Streaming Diarization State Management**: Flink's KeyedState can be used to store speaker clustering centers for each meeting room, enabling cross-window speaker consistency tracking.

**Challenge 3: Missing Models for Low-Resource Languages**

Mainstream ASR models support English and Chinese well, but coverage for minority languages, dialects, and specialized terminology is insufficient.

**Countermeasures**:

- **Fine-tuning**: Fine-tune general models using domain-specific data.
- **Hotword Boosting**: Boost the probability of specific vocabulary (e.g., names, product names) during the decoding phase.
- **Hybrid Decoding**: Interpolate general models with n-gram language models to improve domain accuracy.

---

### 6.5 Audio Quality Assessment Pipeline

In audio stream processing systems, real-time monitoring of input audio quality is critical for early detection of equipment failures or network anomalies.

```java
public class AudioQualityMonitorFunction extends ProcessFunction<AudioFrame, QualityMetric> {
    @Override
    public void processElement(AudioFrame frame, Context ctx, Collector<QualityMetric> out) {
        double[] samples = frame.getSamples();

        // 1. Compute RMS energy
        double rms = Math.sqrt(Arrays.stream(samples).map(s -> s * s).average().orElse(0));

        // 2. Estimate SNR (simplified: based on silence segment assumption)
        double noiseFloor = estimateNoiseFloor(samples);
        double snrDb = 20 * Math.log10(rms / (noiseFloor + 1e-10));

        // 3. Detect clipping
        long clipCount = Arrays.stream(samples)
            .filter(s -> Math.abs(s) > 0.99).count();
        double clipRatio = (double) clipCount / samples.length;

        // 4. Detect DC offset
        double dcOffset = Arrays.stream(samples).average().orElse(0);

        out.collect(new QualityMetric(
            frame.getTimestamp(),
            rms,
            snrDb,
            clipRatio,
            dcOffset
        ));
    }

    private double estimateNoiseFloor(double[] samples) {
        // Estimate noise floor using quantile method
        double[] sorted = samples.clone();
        Arrays.sort(sorted);
        double[] magnitudes = Arrays.stream(sorted).map(Math::abs).toArray();
        Arrays.sort(magnitudes);
        return magnitudes[magnitudes.length / 10]; // 10th percentile
    }
}
```

---

### 6.6 Flink State Management in Audio Streams

In long-duration audio monitoring scenarios (e.g., 24x7 call center quality assurance), Flink's state management is needed to maintain speaker identity, session context, and audio quality baselines.

```java
// KeyedState-based speaker tracking operator
public class SpeakerTrackingFunction extends KeyedProcessFunction<String, AudioFrame, SpeakerEvent> {
    // State: active speaker list for current room
    private ListState<SpeakerProfile> speakerState;
    // State: cumulative speaking time per speaker
    private MapState<String, Long> speakingTimeState;
    // State: audio quality history baseline (for anomaly detection)
    private ValueState<QualityBaseline> baselineState;

    @Override
    public void open(Configuration parameters) {
        speakerState = getRuntimeContext().getListState(
            new ListStateDescriptor<>("speakers", SpeakerProfile.class));
        speakingTimeState = getRuntimeContext().getMapState(
            new MapStateDescriptor<>("speaking-time", String.class, Long.class));
        baselineState = getRuntimeContext().getState(
            new ValueStateDescriptor<>("quality-baseline", QualityBaseline.class));
    }

    @Override
    public void processElement(AudioFrame frame, Context ctx, Collector<SpeakerEvent> out)
            throws Exception {
        String roomId = ctx.getCurrentKey();

        // Update speaking time
        String speakerId = frame.getDetectedSpeakerId();
        Long currentTime = speakingTimeState.get(speakerId);
        if (currentTime == null) currentTime = 0L;
        speakingTimeState.put(speakerId, currentTime + frame.getDurationMs());

        // Update audio quality baseline (exponential moving average)
        QualityBaseline baseline = baselineState.value();
        if (baseline == null) {
            baseline = new QualityBaseline(frame.getRms(), frame.getSnrDb());
        } else {
            baseline.update(frame.getRms(), frame.getSnrDb(), 0.01);
        }
        baselineState.update(baseline);

        // Detect anomaly: current frame SNR deviates from baseline by more than 2 standard deviations
        if (Math.abs(frame.getSnrDb() - baseline.meanSnr) > 2 * baseline.stdSnr) {
            out.collect(new SpeakerEvent(
                roomId, speakerId, "QUALITY_ANOMALY",
                frame.getSnrDb(), ctx.timestamp()
            ));
        }

        // Timer: output session summary once per hour
        long currentHour = ctx.timestamp() / 3_600_000 * 3_600_000;
        ctx.timerService().registerEventTimeTimer(currentHour + 3_600_000);
    }

    @Override
    public void onTimer(long timestamp, OnTimerContext ctx, Collector<SpeakerEvent> out)
            throws Exception {
        String roomId = ctx.getCurrentKey();
        for (Map.Entry<String, Long> entry : speakingTimeState.entries()) {
            out.collect(new SpeakerEvent(
                roomId, entry.getKey(), "HOURLY_SUMMARY",
                entry.getValue(), timestamp
            ));
        }
    }
}
```

**Design Points**:

- Use `KeyedProcessFunction` partitioned by room ID to ensure speaker state consistency within the same room.
- `MapState` is suitable for storing dynamic numbers of speaker information, avoiding pre-allocation of fixed-size state.
- Hourly timers enable periodic session summary output without requiring additional batch jobs.

---

### 6.7 Audio Stream Pipeline Deployment Configuration

Below is a complete Flink audio stream processing job deployment configuration on Kubernetes, including resource limits, checkpoint configuration, and PVC mounting (for storing speech models):

```yaml
apiVersion: flink.apache.org/v1beta1
kind: FlinkDeployment
metadata:
  name: audio-stream-pipeline
spec:
  image: flink:1.18-scala_2.12
  flinkVersion: v1.18
  jobManager:
    resource:
      memory: 2Gi
      cpu: 1
  taskManager:
    resource:
      memory: 4Gi
      cpu: 2
    podTemplate:
      spec:
        containers:
          - name: flink-main-container
            volumeMounts:
              - name: model-volume
                mountPath: /opt/models
        volumes:
          - name: model-volume
            persistentVolumeClaim:
              claimName: audio-models-pvc
  job:
    jarURI: local:///opt/flink/usrlib/audio-pipeline.jar
    parallelism: 4
    upgradeMode: stateful
    state: running
    args:
      - --checkpointing.interval
      - 30s
      - --state.backend
      - rocksdb
      - --state.checkpoints.dir
      - s3://flink-checkpoints/audio-pipeline
```

---

## 7. Visualizations

### 7.1 Audio Stream Processing Decision Tree

```mermaid
flowchart TD
    Start[Audio Input] --> Q1{Application Scenario?}
    Q1 -->|Voice Interaction| ASR[ASR Pipeline<br/>VAD + Feature Extraction + End-to-End Model]
    Q1 -->|Music Analysis| Music[Music Information Retrieval<br/>Beat Detection + Genre Classification]
    Q1 -->|Industrial Monitoring| Anomaly[Anomaly Sound Detection<br/>Spectral Features + Autoencoder]

    ASR --> Latency{Latency Requirement?}
    Latency -->|< 100ms| Edge[Edge Inference]
    Latency -->|> 200ms| Cloud[Cloud Large Model]

    Music --> Q2{Real-Time?}
    Q2 -->|Real-Time| Realtime[Sliding Window Analysis]
    Q2 -->|Offline| Batch[Full Track Analysis]
```

### 7.2 Audio Stream Quality Monitoring Dashboard Architecture

```mermaid
graph LR
    A[Audio Source] --> B[Flink Quality Monitoring]
    B --> C{RMS?}
    C -->|Too Low| D[Silence Alert]
    C -->|Normal| E[SNR Detection]
    E -->|SNR<10dB| F[Noise Alert]
    E -->|SNR>10dB| G[Clipping Detection]
    G -->|Clipping>1%| H[Equipment Failure Alert]
    G -->|Normal| I[High-Quality Audio Stream]
    D --> J[Grafana Dashboard]
    F --> J
    H --> J
    I --> J
```

---

## 8. References

---

*Document Version: v1.0 | Created: 2026-04-19*
