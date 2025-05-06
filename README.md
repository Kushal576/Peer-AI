# Peer-AI: Distributed Machine Learning over 5G P2P Networks

Peer-AI is a distributed machine learning (ML) framework designed for secure, privacy-preserving, and collaborative model training across a decentralized peer-to-peer (P2P) network. The system leverages 5G Device-to-Device (D2D) communication-specifically URLLC and eMBB features-to enable efficient ML training on edge devices without relying on centralized servers.

---

## Features

- **Distributed ML Training:** Decentralized model training using a P2P network architecture, reducing bottlenecks and improving scalability.
- **5G D2D Optimization:** Utilizes 5G's low-latency, high-bandwidth D2D communication for fast and reliable data/model exchange between edge devices.
- **Privacy Preservation:** Implements differential privacy and secure aggregation to protect user data during collaborative training.
- **Byzantine Fault Tolerance:** Uses Krum defense to filter out malicious or faulty updates.
- **Blockchain Integration:** Maintains a tamper-proof ledger of model updates for transparency and auditability.
- **Scalable & Robust:** Designed to scale with additional nodes and remain resilient to node failures or network disruptions.

---

## Motivation

Traditional centralized ML faces challenges like computation bottlenecks, privacy risks, and limited data diversity. Peer-AI addresses these by distributing computation and enabling private, collaborative training-especially relevant as 5G networks make high-speed, direct device communication practical at scale.

---

## System Architecture

### Network Design

- **P2P Network:** Devices connect directly (D2D) when in range, bypassing base stations for lower latency.
- **5G Modes:**  
  - *Infrastructure Mode*: Via base stations (for distant nodes).  
  - *D2D Relay Mode*: Uses intermediary nodes to extend range and boost throughput.  
  - *D2D Non-Relay Mode*: Direct device-to-device for minimal delay.
- **Node Roles:**  
  - *Training Nodes*: Train models locally on private data, add noise for privacy.
  - *Verifying Nodes*: Validate updates using Krum.
  - *Aggregating Nodes*: Aggregate verified updates (FedAvg) and update the global model on blockchain.

---

## Training Workflow

1. **Initialization:** Initiator node distributes the model and starts the blockchain ledger.
2. **Local Training:** Each node trains the model on local data, applying differential privacy.
3. **Verification:** Updates are checked using Krum to filter out malicious contributions.
4. **Aggregation:** Verified updates are aggregated (FedAvg) and recorded on the blockchain.
5. **Iteration:** Process repeats for multiple epochs.

---

## 5G Integration

- **Why 5G?**  
  - *High Throughput*: Supports rapid model update exchange.
  - *Low Latency*: Enables near real-time collaboration.
  - *Massive Connectivity*: Supports large-scale edge participation.
- **Experimental Insights:**  
  - D2D relay mode offers higher throughput at greater distances; non-relay mode provides the lowest latency for close-range devices.
  - D2D communication is generally preferable for distributed ML, with relay mode optimizing throughput and direct mode minimizing delay.

---

## Implementation

- **Framework:** Python, PyTorch for ML, Flask for networking, custom blockchain for update tracking.
- **Algorithms:** SGD, AdaGrad, FedAvg, differential privacy (Gaussian mechanism), Krum defense.
- **Simulation:** 5G network simulated using ns-3; cloud deployment tested on Azure.
- **Benchmark:** MNIST digit classification task demonstrates reduced training time, fast convergence, and robust accuracy.

---

## Results

- **Performance:** Distributed training reduces training time and improves convergence without sacrificing accuracy.
- **Privacy:** Differential privacy effectively protects against gradient leakage.
- **Scalability:** Architecture handles more nodes and remains robust to failures.
- **5G Impact:** D2D communication provides the bandwidth and latency needed for practical distributed ML.

---

## Limitations & Future Work

- **5G Simulation:** Full real-world 5G deployment is pending; current results are based on simulation and cloud P2P.
- **Future Directions:**  
  - Real-world 5G deployment and deeper edge computing integration.
  - Enhanced privacy/security mechanisms.
  - Pilots in healthcare, finance, and smart city domains.

---

## Getting Started

1. **Clone the Repository**
    ```
    git clone <repo-url>
    cd peer-ai
    ```
2. **Install Requirements**
    ```
    pip install -r requirements.txt
    ```
3. **Configure Nodes**
   - Set up training, verifying, and aggregating nodes as described in the documentation.
4. **Run Simulations**
   - Use provided scripts to simulate P2P training and 5G network conditions.
5. **Monitor Training**
   - Access the Flask web interface for training management and monitoring.

---

## Citation

If you use Peer-AI in your research, please cite the original project report and acknowledge the Department of Electronics and Computer Engineering, Pulchowk Campus, Institute of Engineering.

---

**Peer-AI: Democratizing distributed machine learning with 5G-powered, privacy-preserving P2P collaboration.**

---

*For detailed methodology, results, and references, see the attached project report.*

