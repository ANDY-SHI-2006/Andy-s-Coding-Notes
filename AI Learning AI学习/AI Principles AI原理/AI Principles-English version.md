# AI Principles — Introduction to Large AI Models

> **Course:** SCI 1003: Introduction to Large AI Models  
> **Instructor:** Dr. Chi Zhang @ Westlake AGI Lab  
> **Notes Style:** Technical reference with formulas, code snippets, and key concept callouts.

---

# 1 Machine Learning Foundations

## 1.1 What is AI?

In most modern scenarios, **AI refers to Deep Learning**.

**Machine Learning** can be understood as:

> **Key Concept:** Machine Learning ≈ Looking for a Function  
> We want to find a function `f` that maps inputs `x` to desired outputs `y`:
> ```
> y = f(x)
> ```
> The function is learned from data rather than explicitly programmed.

### 1.1.1 The Three Steps of Machine Learning

| Step | Action | Description |
|------|--------|-------------|
| **1** | Define a function with unknown parameters | Choose model architecture (e.g., linear, neural network) |
| **2** | Define loss from training data | Measure how bad the function performs on known data |
| **3** | Optimization | Adjust parameters to minimize the loss |

```
Training Data: (x₁, ŷ₁), (x₂, ŷ₂), ..., (xₙ, ŷₙ)
                        ↓
Step 1: y = f_θ(x)   [Function with parameters θ]
                        ↓
Step 2: L(θ)         [Loss function]
                        ↓
Step 3: θ* = argmin_θ L(θ)  [Optimization]
                        ↓
Use y = f_θ*(x) to label testing data
```

## 1.2 Linear Regression

### 1.2.1 The Linear Model

For a simple 2D case:

```
Input x:  tensor with shape (1, 2)  — each data point
Output y: predicted value/label
Weight W: learnable parameter with shape (1, 2)
Bias b:   learnable scalar with shape (1,)
```

**Prediction:**
```
y = W · x + b
```

In matrix form:
```
ŷ = Wx + b
```

### 1.2.2 Loss Function

For linear regression, we use **Mean Squared Error (MSE)**:

```
L = (1/N) Σₙ (ŷₙ - yₙ)²
```

Where:
- `ŷₙ` is the predicted value
- `yₙ` is the ground-truth label
- `N` is the number of training samples

### 1.2.3 Gradient Descent Optimization

> **Key Concept:** Gradient Descent iteratively updates parameters in the direction that reduces loss.

**Algorithm:**

1. (Randomly) pick an initial value `w₀`
2. Compute gradient: `∂L/∂w |_{w=w₀}`
3. Update: `w₁ ← w₀ - η(∂L/∂w)`
4. Repeat until convergence

```
        Loss L
          │    ╲      global
          │     ╲     minima
          │      ╲   /
          │       ╲_/
          │   w*  /
          │___/___/________
              w₀  w₁  w
```

Where `η` (eta) is the **learning rate** — a hyperparameter controlling step size.

> **Key Point:** If the learning rate is too large, optimization may diverge. If too small, convergence is very slow.

### 1.2.4 Learning Rate Decay

A fixed learning rate may cause oscillations near the minimum. **Learning Rate Decay** gradually reduces `η` over time:

```
η_t = η₀ / (1 + decay_rate × epoch)
```

| Strategy | Behavior |
|----------|----------|
| Fixed LR | Constant step size |
| Step decay | Reduce LR by factor every N epochs |
| Exponential decay | `η_t = η₀ × e^(-kt)` |

## 1.3 Logistic Regression

### 1.3.1 Why Not Linear Regression for Classification?

Using MSE with labels {0, 1} has problems:
- Predictions outside [0, 1] are penalized even if classification is correct
- Not a natural fit for probability outputs

### 1.3.2 The Sigmoid Function

```
σ(z) = 1 / (1 + e^(-z))
```

Properties:
- Output range: (0, 1)
- Can be interpreted as probability
- Differentiable everywhere

**Logistic Regression Model:**
```
ŷ = σ(Wx + b) = 1 / (1 + e^-(Wx+b))
```

### 1.3.3 Binary Cross-Entropy Loss

```
L = -(1/N) Σₙ [yₙ log(ŷₙ) + (1-yₙ) log(1-ŷₙ)]
```

> **Key Concept:** Minimizing cross-entropy is equivalent to maximizing the likelihood of the observed data.

## 1.4 Neural Networks

### 1.4.1 Motivation: Limitations of Linear Models

Linear models have severe limitations — they can only learn linear decision boundaries. Many real-world problems require non-linear separation.

### 1.4.2 Building Neural Networks with Sigmoid Neurons

A complex curve can be approximated by a sum of multiple sigmoid functions:

```
y = b + Σᵢ cᵢ · σ(bᵢ + wᵢx)
```

Where each `σ(bᵢ + wᵢx)` is a "sigmoid neuron" that can be shifted and scaled:

| Parameter | Effect |
|-----------|--------|
| `w` | Changes slope/steepness |
| `b` | Shifts left/right |
| `c` | Changes height/amplitude |

### 1.4.3 Neural Network as Matrix Multiplication + Activation

For multiple inputs and multiple neurons:

```
r = b + Wx
a = σ(r)
y = cᵀa + b'
```

In full matrix form for a layer:

```
Input x        Weight W       Bias b      Activation σ
  │               │              │              │
  ▼               ▼              ▼              ▼
[x₁]          [w₁₁ w₁₂]      [b₁]         [σ(r₁)]
[x₂]    ×     [w₂₁ w₂₂]  +   [b₂]    →    [σ(r₂)]
[x₃]          [w₃₁ w₃₂]      [b₃]         [σ(r₃)]
```

> **Key Concept:** Neural Networks are simply **matrix multiplication + activation function**, repeated layer after layer.

### 1.4.4 Forward Pass and Backpropagation

**Forward Pass:** Compute output layer by layer from input to output.

**Backpropagation:** Use the **chain rule** to compute gradients backward from output to input.

```
Forward:  x → [Layer 1] → [Layer 2] → ... → [Layer N] → ŷ
Backward: ∂L/∂ŷ ← [Layer N] ← ... ← [Layer 2] ← [Layer 1]
```

**Chain Rule Example:**
```
If y = f(g(x)), then dy/dx = f'(g(x)) · g'(x)
```

### 1.4.5 Summary: What is a Neural Network?

> **Key Concept:**
> - Each node/neuron has its meaning (learns a feature)
> - NNs are hard to explain (black box nature)
> - NNs are simply matrix multiplication + activation function
> - Layer outputs are **features of data** — middle layers extract features, only the last layer is the classifier

---

# 2 Training Deep Neural Networks

## 2.1 Overfitting

### 2.1.1 Definition

> **Key Concept:** Overfitting = Small loss on training data, large loss on testing data.

**Extreme Example — The "Remember" Function:**
```
f(x) = { ŷᵢ   if ∃xᵢ = x  (exact match in training)
       { random  otherwise
```

This function achieves zero training loss but is useless for prediction.

### 2.1.2 Bias-Complexity Trade-off

```
        loss
          │╲    Testing loss
          │ ╲___/
          │   ↑    ← select this model
          │  / ╲
          │ /   ╲  Training loss
          │/     ╲________
          └────────────────→ Model complexity
                (more parameters)
```

> **Key Point:** As model complexity increases, training loss always decreases, but testing loss first decreases then increases. The goal is to find the "sweet spot."

## 2.2 Regularization Techniques

### 2.2.1 Dropout

During training, randomly disable (set to zero) a subset of neurons at each iteration.

| Phase | Behavior |
|-------|----------|
| **Training** | Random subset of neurons disabled (e.g., 50% dropout rate) |
| **Inference** | All neurons active; outputs scaled by dropout rate |

> **Key Point:** Dropout prevents neurons from co-adapting too strongly, forcing the network to learn redundant representations.

### 2.2.2 Data Augmentation

Artificially expand training data by applying transformations:

| Modality | Common Augmentations |
|----------|---------------------|
| **Images** | Random crop, horizontal flip, rotation, color jitter, scaling |
| **Tabular** | Adding noise, synthetic sampling (SMOTE) |
| **Text** | Synonym replacement, back-translation |

PyTorch example:
```python
import torchvision.transforms as transforms

transform = transforms.Compose([
    transforms.RandomCrop(32, padding=4),
    transforms.RandomHorizontalFlip(),
    transforms.ToTensor(),
])
```

## 2.3 Cross Validation

### 2.3.1 Train-Validation-Test Split

| Set | Purpose |
|-----|---------|
| **Training Set** | Update model parameters |
| **Validation Set** | Tune hyperparameters, select model |
| **Test Set** | Final unbiased evaluation |

### 2.3.2 N-Fold Cross Validation

```
Fold 1: [Val][Train][Train][Train][Train] → Model 1
Fold 2: [Train][Val][Train][Train][Train] → Model 2
Fold 3: [Train][Train][Val][Train][Train] → Model 3
...
```

1. Split training data into N folds
2. Train N models, each using one fold as validation
3. Average validation performance across all folds
4. Select hyperparameters with best average score

## 2.4 Batch Training

### 2.4.1 Gradient Descent Variants

| Method | Update Frequency | Speed per Update | Gradient Quality |
|--------|-----------------|------------------|------------------|
| **Batch GD** | After all samples | Slow | Stable (exact) |
| **Mini-batch GD** | After N samples | Fast | Noisy but efficient |
| **Stochastic GD** | After each sample | Very fast | Very noisy |

In deep learning, **mini-batch gradient descent** is standard.

### 2.4.2 Small Batch vs Large Batch

| Aspect | Small Batch | Large Batch |
|--------|-------------|-------------|
| Speed per update (no parallel) | Faster | Slower |
| Speed per update (with GPU) | Same | Same (up to memory limit) |
| Time for one epoch | Slower | Faster |
| Gradient | Noisy | Stable |
| Optimization | Better (escapes sharp minima) | Worse (may get stuck) |
| Generalization | Better | Worse |

> **Key Point:** "Noisy" updates from small batches help escape sharp local minima and find flatter minima that generalize better.

### 2.4.3 Epochs and Iterations

```
1 epoch = seeing all training samples once

If dataset has 60,000 samples and batch_size = 64:
- Iterations per epoch = 60,000 / 64 ≈ 938
```

> **Best Practice:** Shuffle data after each epoch to prevent the model from learning order-dependent patterns.

## 2.5 Advanced Optimization

### 2.5.1 Gradient Descent with Momentum

Instead of moving purely by current gradient, accumulate movement from previous steps:

```
m₀ = 0
m_t = λ·m_{t-1} - η·g_t   (movement)
θ_t = θ_{t-1} + m_t       (parameter update)
```

Where:
- `λ` (lambda): momentum coefficient (typically 0.9)
- `g_t`: gradient at step t
- `m_t`: accumulated movement

> **Key Concept:** Momentum helps accelerate in consistent directions and dampens oscillations, similar to a ball rolling down a hill with inertia.

### 2.5.2 Common Optimizers

| Optimizer | Key Feature | Use Case |
|-----------|-------------|----------|
| **SGD** | Basic gradient descent | Simple, well-understood |
| **SGD + Momentum** | Adds velocity term | Faster convergence |
| **Adam** | Adaptive learning rates per parameter | Default choice for most tasks |
| **AdamW** | Adam with decoupled weight decay | Often better than Adam |

PyTorch usage:
```python
import torch.optim as optim

# SGD with momentum
optimizer = optim.SGD(model.parameters(), lr=0.01, momentum=0.9)

# Adam
optimizer = optim.Adam(model.parameters(), lr=0.001)
```

## 2.6 Multi-Class Classification

### 2.6.1 One-Hot Encoding

Classes are represented as one-hot vectors:

```
Class 1: [1, 0, 0]
Class 2: [0, 1, 0]
Class 3: [0, 0, 1]
```

### 2.6.2 Softmax Function

Converts raw logits to probabilities:

```
y'ᵢ = exp(yᵢ) / Σⱼ exp(yⱼ)
```

Properties:
- Each output is between 0 and 1
- All outputs sum to 1
- Amplifies differences (larger logits → more confident predictions)

### 2.6.3 Cross-Entropy Loss for Classification

```
L = -(1/N) Σₙ Σᵢ ŷₙ,ᵢ · log(y'ₙ,ᵢ)
```

Where `ŷ` is the one-hot ground truth and `y'` is the softmax output.

> **Key Concept:** Cross-entropy loss provides stronger gradients than MSE for classification, especially when predictions are far from correct. MSE can lead to vanishing gradients in early training.

### 2.6.4 Training Loop in PyTorch

```python
for epoch in range(num_epochs):
    model.train()
    for inputs, labels in train_loader:
        optimizer.zero_grad()      # Clear previous gradients
        outputs = model(inputs)    # Forward pass
        loss = criterion(outputs, labels)  # Compute loss
        loss.backward()            # Backpropagation
        optimizer.step()           # Update parameters
```



---

# 3 Convolutional Neural Networks (CNNs)

## 3.1 From Fully Connected to Convolutional

### 3.1.1 Why Not Fully Connected for Images?

A 100×100 RGB image has 100 × 100 × 3 = 30,000 input values. A fully connected layer to 1000 neurons would require 30 million weights — enormous and impractical.

> **Key Concept:** Images have spatial structure. Nearby pixels are correlated, and the same patterns appear in different regions. CNNs exploit these properties.

### 3.1.2 Three Key Observations

| Observation | Insight | CNN Solution |
|-------------|---------|--------------|
| **1. Local patterns** | Some patterns (edges, textures) are much smaller than the whole image | **Receptive Field**: each neuron only sees a local patch |
| **2. Same patterns everywhere** | The same feature (e.g., a beak detector) is useful in any region | **Parameter Sharing**: same filter applied across the image |
| **3. Subsampling works** | Downsampling the image doesn't change the object | **Pooling**: reduce spatial dimensions |

## 3.2 Convolution Operation

### 3.2.1 Filter / Kernel

A filter is a small weight matrix (e.g., 3×3) that slides across the image, computing dot products at each position.

```
Input Image (6×6)          Filter (3×3)            Feature Map
┌──┬──┬──┬──┬──┬──┐       ┌──┬──┬──┐
│ 1│ 0│ 0│ 0│ 0│ 1│       │ 1│-1│-1│
├──┼──┼──┼──┼──┼──┤       ├──┼──┼──┤
│ 0│ 1│ 0│ 0│ 1│ 0│   *   │-1│ 1│-1│   →   (4×4 output)
├──┼──┼──┼──┼──┼──┤       ├──┼──┼──┤
│ 0│ 0│ 1│ 1│ 0│ 0│       │-1│-1│ 1│
├──┼──┼──┼──┼──┼──┤       └──┴──┴──┘
│ 0│ 0│ 1│ 1│ 0│ 0│
├──┼──┼──┼──┼──┼──┤
│ 0│ 1│ 0│ 0│ 1│ 0│
├──┼──┼──┼──┼──┼──┤
│ 1│ 0│ 0│ 0│ 0│ 1│
└──┴──┴──┴──┴──┴──┘
```

> **Key Concept:** Each filter detects a specific small pattern. Multiple filters produce multiple feature maps (channels).

### 3.2.2 Hyperparameters of Convolution

| Parameter | Description | Typical Value |
|-----------|-------------|---------------|
| **Kernel size** | Size of the filter | 3×3, 5×5, 7×7 |
| **Stride** | How many pixels the filter moves | 1 or 2 |
| **Padding** | Zeros added around the image border | 0, 1, or "same" |
| **Channels** | Number of input/output feature maps | 1 (grayscale), 3 (RGB), 64, 128, 256... |

**Output size formula:**
```
Output = floor((Input - Kernel + 2×Padding) / Stride) + 1
```

### 3.2.3 Two Equivalent Stories

| Neuron Story | Filter Story |
|--------------|--------------|
| Each neuron only considers a receptive field | There are a set of filters detecting small patterns |
| Neurons with different receptive fields share parameters | Each filter convolves over the entire input image |

> **Key Point:** These are the same story told two different ways. The "filter" view is more common in deep learning frameworks.

## 3.3 Pooling

### 3.3.1 Max Pooling

```
Feature Map (4×4)          Pooled (2×2)
┌──┬──┬──┬──┐              ┌──┬──┐
│ 3│-1│-3│-1│    2×2       │ 3│ 1│
├──┼──┼──┼──┤   pool       ├──┼──┤
│-3│ 1│ 0│-3│   stride=2   │ 3│ 3│
├──┼──┼──┼──┤   →          └──┴──┘
│-3│-3│ 0│ 1│
├──┼──┼──┼──┤
│ 3│-2│-2│-1│
└──┴──┴──┴──┘
```

> **Key Concept:** Pooling reduces spatial dimensions while keeping the most salient activation. It provides **translation invariance** — small shifts in the input don't change the output much.

### 3.3.2 Typical CNN Architecture

```
Input Image
    ↓
[Convolution + ReLU]  → Feature maps
    ↓
[Max Pooling]         → Downsampling
    ↓
[Convolution + ReLU]  → More abstract features
    ↓
[Max Pooling]         → Further downsampling
    ↓
[Flatten]             → Vector
    ↓
[Fully Connected]     → Classification
    ↓
[Softmax]             → Class probabilities
```

## 3.4 Classic CNN Architectures

### 3.4.1 LeNet-5 (1998)

Developed by Yann LeCun et al. for handwritten digit recognition.

| Layer | Type | Details |
|-------|------|---------|
| C1 | Convolution | 6 filters, 5×5, stride 1 |
| S2 | Subsampling (Avg Pool) | 2×2 |
| C3 | Convolution | 16 filters, 5×5 |
| S4 | Subsampling | 2×2 |
| C5 | Convolution (FC-like) | 120 filters |
| F6 | Fully Connected | 84 units |
| Output | RBF | 10 classes |

### 3.4.2 AlexNet (2012)

Developed by Alex Krizhevsky, Ilya Sutskever, and Geoffrey Hinton. Won ImageNet 2012 — the breakthrough moment for deep learning.

**Key Innovations:**

| Innovation | Significance |
|------------|--------------|
| **ReLU Activation** | Faster training than sigmoid/tanh; mitigates vanishing gradients |
| **GPU Training** | First to leverage GPUs for large-scale CNN training (2× GTX 580) |
| **Dropout** | 50% dropout in FC layers to reduce overfitting |
| **Data Augmentation** | Random crops, horizontal flips to improve generalization |
| **Overlapping Max Pooling** | Better feature preservation |

**Architecture:** 8 layers (5 conv + 3 FC)

> **Key Point:** After AlexNet's success, traditional computer vision methods (SIFT, HOG) virtually disappeared from ImageNet leaderboards.

### 3.4.3 VGGNet (2014)

Developed by the Visual Geometry Group at Oxford.

**Core Idea:** Make CNNs deeper using a very simple, uniform architecture.

| Feature | Description |
|---------|-------------|
| **Small filters** | Only 3×3 convolutions (stacked to increase receptive field) |
| **Deep** | VGG-16 (16 layers), VGG-19 (19 layers) |
| **Uniform** | Same pattern: conv → conv → [optional conv] → max pool |

> **Key Concept:** Two stacked 3×3 filters have the same receptive field as one 5×5 filter, but with fewer parameters (2×3²=18 vs 5²=25) and more nonlinearity.

## 3.5 ResNet: Deep Residual Learning

### 3.5.1 The Degradation Problem

As networks get deeper:
- **Vanishing/Exploding Gradients**: Gradients become extremely small or large
- **Degradation Problem**: Deeper networks should perform better, but in practice they often perform worse on training data (not just overfitting!)

> **Key Concept:** The degradation problem suggests that deeper networks are harder to optimize, not just prone to overfitting.

### 3.5.2 Residual Block

Instead of learning `H(x)` directly, learn the **residual** `F(x) = H(x) - x`:

```
        x ───────────────┐
          │               │
          ▼               │
    [Conv → BN → ReLU]    │
          │               │
          ▼               │ Identity
    [Conv → BN]           │ Shortcut
          │               │
          ▼               │
        F(x)              │
          │               │
          ▼               │
      F(x) + x ◄──────────┘
          │
          ▼
        ReLU
```

> **Key Concept:** The identity shortcut allows gradients to flow directly through the network. If the optimal mapping is close to identity, the network only needs to learn small residual corrections.

### 3.5.3 Impact of ResNet

| Area | Impact |
|------|--------|
| **Image Recognition** | Outperformed VGG with fewer parameters; became default feature extractor |
| **New Architectures** | Inspired ResNeXt, DenseNet, EfficientNet |
| **Beyond Vision** | Transformers (BERT, GPT, ViT) all use residual connections |
| **Applications** | NLP, speech recognition, medical imaging, autonomous driving |

---

# 4 Advanced CNN Techniques

## 4.1 Global Average Pooling (GAP)

Instead of flattening the final feature maps and feeding them to a large fully connected layer:

```
Traditional:  Feature Maps (512×7×7) → Flatten (25088) → FC (4096) → FC (1000)
GAP:          Feature Maps (512×7×7) → AvgPool → 512-dim vector → FC (1000)
```

| Advantage | Explanation |
|-----------|-------------|
| **No parameters** | Averaging has no learnable weights |
| **Less overfitting** | Removes the large parameter-heavy FC layer |
| **Better localization** | Each feature map directly corresponds to a class |

## 4.2 Class Activation Maps (CAM)

CAM visualizes which regions of an image the CNN focuses on for classification.

**Method (with GAP):**
```
1. Forward pass to get final conv feature maps A_k (K channels)
2. Get FC weights w_k for target class
3. CAM = Σ_k w_k × A_k
4. Upsample CAM to image size and overlay as heatmap
```

```python
# Simplified CAM implementation
cam = torch.zeros(feature_maps.shape[2:])
for i in range(fc_weights.shape[0]):
    cam += fc_weights[i] * feature_maps[0, i, :, :]
cam = cv2.resize(cam.numpy(), (224, 224))
```

> **Key Point:** CAM reveals that CNNs naturally learn to localize objects without explicit bounding box supervision.

## 4.3 Pretrained CNNs as Backbones

A **backbone** is a pretrained CNN used as a feature extractor for downstream tasks:

| Task | Approach |
|------|----------|
| **Metric Learning** | Use layer embeddings for similarity search |
| **Object Detection** | Extract features → region proposals → classify & refine |
| **Image Segmentation** | Encode-decoder architecture (FCN, U-Net) |
| **Depth Estimation** | Predict depth maps from single images |

## 4.4 Fully Convolutional Networks (FCN)

For dense prediction tasks (segmentation), we need spatial output maps, not just class vectors.

### 4.4.1 Transforming CNN to FCN

Replace fully connected layers with 1×1 convolutions to preserve spatial structure:

```
Traditional CNN:  Image → [Conv layers] → Flatten → FC → Class vector
FCN:              Image → [Conv layers] → 1×1 Conv → Upsample → Pixel-wise labels
```

### 4.4.2 Transposed Convolution

Used to upsample feature maps back to input resolution:

```
Standard Conv:    Input (4×4) → Filter (3×3, stride 2) → Output (2×2)
Transposed Conv:  Input (2×2) → Filter (3×3, stride 2) → Output (4×4)
```

### 4.4.3 U-Net Architecture

Popular for biomedical image segmentation:

```
Encoder (Contracting Path)              Decoder (Expansive Path)
  ┌─────────┐                              ┌─────────┐
  │ Conv×2  │ ─────────── Skip ───────────→│ Concat  │
  │  ↓Pool  │         Connection            │  Conv×2 │
  └─────────┘                              └─────────┘
       ↓                                        ↑
  ┌─────────┐                              ┌─────────┐
  │ Conv×2  │ ─────────── Skip ───────────→│ Concat  │
  │  ↓Pool  │         Connection            │  Conv×2 │
  └─────────┘                              └─────────┘
       ↓                                        ↑
       └────────────── Bottleneck ──────────────┘
```

> **Key Concept:** Skip connections preserve high-resolution spatial information from the encoder, helping the decoder produce precise boundaries.

---

# 5 Sequence Modeling and Self-Attention

## 5.1 Beyond Fixed Inputs

| Input Type | Example | Challenge |
|------------|---------|-----------|
| Single vector | Tabular data, image features | Fixed size — easy |
| Grid of vectors | Images | Fixed grid structure |
| **Set of vectors** | Text, speech, graphs | **Variable length, variable order** |

### 5.1.1 Representing Sequences

**One-Hot Encoding:**
```
apple  = [1, 0, 0, 0, ...]
bag    = [0, 1, 0, 0, ...]
cat    = [0, 0, 1, 0, ...]
```

**Word Embeddings:** Dense, learned vector representations where similar words have similar vectors.

**Audio (Speech):**
```
1 second → 100 frames
Each frame: 39-dim MFCC or 80-dim filter bank output
```

## 5.2 Self-Attention Mechanism

### 5.2.1 The Core Idea

Self-attention allows each position in a sequence to **attend to all other positions**, computing a weighted sum based on relevance.

> **Key Concept:** Self-attention replaces recurrence/convolution with direct pairwise interactions, enabling parallel computation and global receptive field.

### 5.2.2 Query, Key, Value

For each input vector `aᵢ`, compute three projections:

```
qᵢ = W_q · aᵢ    (Query: what am I looking for?)
kᵢ = W_k · aᵢ    (Key: what do I contain?)
vᵢ = W_v · aᵢ    (Value: what information do I provide?)
```

### 5.2.3 Attention Score and Output

```
1. Compute attention scores:  αᵢⱼ = qᵢ · kⱼ

2. Apply softmax normalization:
   α'ᵢⱼ = exp(αᵢⱼ) / Σₗ exp(αᵢₗ)

3. Compute output as weighted sum:
   bᵢ = Σⱼ α'ᵢⱼ · vⱼ
```

**Matrix form (efficient batch computation):**
```
Q = W_q · A        (Query matrix)
K = W_k · A        (Key matrix)
V = W_v · A        (Value matrix)

Attention(Q, K, V) = softmax(QKᵀ / √d_k) · V
```

> **Key Point:** The `√d_k` scaling prevents dot products from growing too large in high dimensions, which would push softmax into extreme regions with small gradients.

### 5.2.4 Self-Attention Layer Structure

```
Input:  [a₁, a₂, a₃, a₄]
           ↓
    ┌─────┴─────┐
    ▼     ▼     ▼
   W_q    W_k   W_v
    │      │      │
    ▼      ▼      ▼
   [Q]    [K]    [V]
    │      │      │
    └──────┼──────┘
           ▼
      QKᵀ / √d_k
           │
           ▼
       softmax
           │
           ▼
        A' (attention weights)
           │
           ▼
        A' × V
           │
           ▼
Output: [b₁, b₂, b₃, b₄]
```

## 5.3 Multi-Head Self-Attention

Instead of one attention computation, use multiple "heads" to capture different types of relationships:

```
Input
  ├──► Head 1: Q₁, K₁, V₁ ──► Attention₁ ──┐
  ├──► Head 2: Q₂, K₂, V₂ ──► Attention₂ ──┼──► Concat ──► Linear ──► Output
  ├──► Head 3: Q₃, K₃, V₃ ──► Attention₃ ──┤
  └──► Head h: Q_h, K_h, V_h ─► Attention_h ┘
```

> **Key Concept:** Different heads can learn different relational patterns (e.g., syntactic vs. semantic relationships in language).

## 5.4 Transformer Encoder

### 5.4.1 Building Block

```
Input + Positional Embedding
           │
           ▼
    ┌─────────────┐
    │ Multi-Head  │
    │ Self-Attn   │
    └─────────────┘
           │
           ▼
      LayerNorm
           │
           ▼
    ┌─────────────┐
    │ Feed-Forward│  (MLP: expand → ReLU → project)
    └─────────────┘
           │
           ▼
      LayerNorm
           │
           ▼
        Output
```

With residual connections around each sub-layer:
```
x' = LayerNorm(x + SelfAttention(x))
output = LayerNorm(x' + MLP(x'))
```

### 5.4.2 Positional Encoding

Transformers have no inherent notion of sequence order. Positional encodings inject position information:

| Type | Description |
|------|-------------|
| **Sinusoidal** | Fixed sine/cosine functions at different frequencies |
| **Learnable** | Learned embedding vectors for each position |

> **Key Point:** In Vision Transformers, learned positional embeddings naturally encode 2D spatial structure — adjacent patches have similar embeddings.

---

# 6 Vision Transformer (ViT)

## 6.1 From CNN to Transformer for Images

### 6.1.1 Motivation

CNNs have strong inductive biases (locality, translation invariance) but struggle to capture **global relationships** without deep stacks of convolutions. Transformers can model global dependencies directly via self-attention.

### 6.1.2 Patch Embedding

Split an image into fixed-size patches and treat them as a sequence:

```
Input Image (224×224×3)
           │
           ▼
    Split into 16×16 patches
           │
           ▼
    14×14 = 196 patches
    Each patch: 16×16×3 = 768-dim vector
           │
           ▼
    Linear projection to embedding dimension D
           │
           ▼
    [Patch 1] [Patch 2] ... [Patch 196]
```

```python
# Conceptual ViT patch embedding
x = image.unfold(2, patch_size, patch_size).unfold(3, patch_size, patch_size)
x = x.flatten(2).transpose(1, 2)  # (B, num_patches, patch_dim)
x = self.patch_embed(x)           # (B, num_patches, embed_dim)
```

## 6.2 ViT Architecture

### 6.2.1 Classification Token [CLS]

```
[CLS]  [Patch 1] [Patch 2] ... [Patch 196]
  │        │         │             │
  ▼        ▼         ▼             ▼
 +Pos    +Pos      +Pos          +Pos
  │        │         │             │
  └────────┴─────────┴─────────────┘
                    │
            Transformer Encoder × L
                    │
  ┌─────────────────┼─────────────────┐
  ▼                 ▼                 ▼
[CLS]          [Patches]        (ignored)
  │
  ▼
MLP Head
  │
  ▼
Class Prediction
```

> **Key Concept:** The [CLS] token aggregates information from all patches through self-attention layers. Its final state serves as the global image representation.

### 6.2.2 Components

| Component | Description |
|-----------|-------------|
| **Patch Embedding** | Linear projection of flattened patches |
| **Positional Embedding** | Learnable 1D embeddings added to each patch |
| **Transformer Encoder** | L layers of Multi-Head Self-Attention + MLP blocks |
| **LayerNorm + Residuals** | Pre-norm configuration for stable training |
| **Classification Head** | MLP attached to [CLS] token for supervised learning |

### 6.2.3 ViT vs ResNets

| Aspect | ResNet | ViT |
|--------|--------|-----|
| **Inductive bias** | Strong (locality, translation invariance) | Weak (must learn spatial structure) |
| **Data efficiency** | Better with small datasets | Requires large pretraining datasets |
| **Global context** | Grows with depth | Immediate in every layer |
| **Computational cost** | Efficient convolutions | Quadratic attention cost |
| **Scaling** | Plateaus sooner | Continues improving with more data |

> **Key Point:** ResNets perform better with smaller pre-training datasets, but ViT surpasses them when trained on very large datasets (ImageNet-21k, JFT-300M).

## 6.3 Hybrid and Hierarchical Vision Transformers

| Model | Key Feature |
|-------|-------------|
| **ViT** | Pure transformer on patches; uniform architecture |
| **Swin Transformer** | Hierarchical windows; shifted window attention for efficiency |
| **MViT** | Multiscale vision transformer; pooling attention |
| **PVT** | Pyramid vision transformer; progressive shrinking |

---

# 7 CLIP and Large Language Models

## 7.1 CLIP: Contrastive Language-Image Pre-training

### 7.1.1 Motivation

| Challenge | Detail |
|-----------|--------|
| NLP breakthroughs | BERT, GPT achieve zero-shot generalization via unsupervised pretraining on web text |
| Vision limitation | Vision models still rely on human-annotated datasets like ImageNet |
| Early attempts | Small-scale image-text pairs showed poor zero-shot performance (~11% on ImageNet) |
| **Key Question** | Can natural language supervision replace labeled datasets if scaled up enough? |

### 7.1.2 Core Insight

> **Key Concept:** Natural language can serve as a general, flexible supervision signal for training vision models. When scaled to hundreds of millions of image-text pairs, this enables learning of generalizable image representations.

### 7.1.3 Dataset: WebImageText (WIT)

| Property | Detail |
|----------|--------|
| **Scale** | 400 million (image, text) pairs |
| **Source** | Public internet sources |
| **Query diversity** | 500,000 search queries (words appearing ≥100 times in English Wikipedia) |
| **Per-query limit** | Max 20,000 pairs per query to ensure diversity |

### 7.1.4 Contrastive Learning

Instead of predicting the exact caption word-by-word (generative, slow), CLIP learns to **match images with their correct text** among many options:

```
                Text Embeddings
                [T₁] [T₂] [T₃] ... [Tₙ]
                    │   │   │       │
Image Embeddings    ▼   ▼   ▼       ▼
[I₁] ─────────→  [✓]  [✗]  [✗] ... [✗]
[I₂] ─────────→  [✗]  [✓]  [✗] ... [✗]
[I₃] ─────────→  [✗]  [✗]  [✓] ... [✗]
 ...
[Iₙ] ─────────→  [✗]  [✗]  [✗] ... [✓]

Objective: Maximize similarity on diagonal (correct pairs),
           minimize similarity off-diagonal (incorrect pairs)
```

**InfoNCE Loss:**
```
L = -log(exp(sim(Iᵢ, Tᵢ)/τ) / Σⱼ exp(sim(Iᵢ, Tⱼ)/τ))
```

Where `sim` is cosine similarity and `τ` is a learned temperature parameter.

> **Key Point:** Contrastive learning is ~4× more training-efficient than caption prediction.

### 7.1.5 Architecture

| Component | Configuration |
|-----------|---------------|
| **Image Encoder** | ResNet-50 (with attention pooling) or ViT |
| **Text Encoder** | Transformer (12 layers, 8 heads, 63M parameters) |
| **Tokenizer** | BPE (Byte Pair Encoding) |
| **Projection** | Linear layers to shared embedding space |

### 7.1.6 Zero-Shot Classification

At test time, CLIP synthesizes a zero-shot classifier:

```python
# Encode image
image_features = model.encode_image(image)

# Encode class descriptions
texts = [f"a photo of a {label}" for label in class_names]
text_features = model.encode_text(texts)

# Compute similarity
similarities = image_features @ text_features.T
predicted_class = similarities.argmax()
```

> **Best Practice:** The prompt template `"A photo of a {label}."` is a good default. Adding domain context (e.g., `"a type of food"`) helps with fine-grained tasks.

### 7.1.7 Applications

| Application | How CLIP Helps |
|-------------|----------------|
| **Zero-shot classification** | No task-specific training needed |
| **Image-text retrieval** | Find images matching text queries and vice versa |
| **Object detection** | Text queries guide object localization |
| **Text-to-image generation** | DALL-E, Stable Diffusion use CLIP for alignment |

## 7.2 Tokenization: Byte Pair Encoding (BPE)

### 7.2.1 Why BPE?

| Approach | Problem |
|----------|---------|
| Word-level | Huge vocabulary; OOV (out-of-vocabulary) words |
| Character-level | Very long sequences; loses word-level meaning |
| **BPE** | Balanced: compact vocabulary + handles any word |

### 7.2.2 BPE Algorithm

```
Training Phase:
1. Start with character vocabulary
2. Count adjacent symbol pairs in corpus
3. Merge the most frequent pair
4. Add merged symbol to vocabulary
5. Repeat until desired vocabulary size

Example Corpus: "low low low lower newest widest"
Initial:  l, o, w, e, r, n, s, t, i, d
Merge 1:  e+s → es  (most frequent)
Merge 2:  es+t → est
Merge 3:  est+</w> → est</w>
Merge 4:  l+o → lo
Merge 5:  lo+w → low
...
```

**Encoding (inference):**
```
Input: "lowest"
Split: ['l', 'o', 'w', 'e', 's', 't', '</w>']
Apply merges in order:
  e+s → es      : ['l', 'o', 'w', 'es', 't', '</w>']
  es+t → est    : ['l', 'o', 'w', 'est', '</w>']
  est+</w> → est</w> : ['l', 'o', 'w', 'est</w>']
  l+o → lo      : ['lo', 'w', 'est</w>']
  lo+w → low    : ['low', 'est</w>']
Output: ["low", "est</w>"]
```

> **Key Concept:** BPE solves the OOV problem by breaking unknown words into known subwords. "lowest" was never seen in training, but splits into meaningful subwords "low" + "est".

## 7.3 GPT: Generative Pre-trained Transformer

### 7.3.1 Architecture

GPT is a **decoder-only** autoregressive language model:

```
Original Transformer Decoder          GPT Decoder-only
┌─────────────────┐                  ┌─────────────────┐
│ Self-Attention  │                  │ Masked Self-Attn│
│ (Masked)        │                  │                 │
├─────────────────┤                  ├─────────────────┤
│ Cross-Attention │    ───Remove──→  │   (Removed)     │
│ (with Encoder)  │                  │                 │
├─────────────────┤                  ├─────────────────┤
│ Feed-Forward    │                  │ Feed-Forward    │
└─────────────────┘                  └─────────────────┘
```

> **Key Point:** GPT removes cross-attention because there is no encoder input — the model only attends to previously generated tokens.

### 7.3.2 Next-Word Prediction

GPT is trained to predict the next token given all previous tokens:

```
Input:  "The cat sat on the"
Target:                      "mat"

P("mat" | "The", "cat", "sat", "on", "the")
```

**Autoregressive generation:**
```
Step 1: Input "The"          → Predict "cat"
Step 2: Input "The cat"      → Predict "sat"
Step 3: Input "The cat sat"  → Predict "on"
...
```

```python
# Autoregressive text generation
def generate(model, prompt, max_length=50):
    tokens = tokenize(prompt)
    for _ in range(max_length):
        logits = model(tokens)
        next_token = sample(logits[-1])  # predict next
        tokens.append(next_token)
    return detokenize(tokens)
```

### 7.3.3 In-Context Learning

GPT-3's breakthrough: the model can learn from examples provided in the prompt, without updating any parameters.

| Type | Format | Example |
|------|--------|---------|
| **Zero-shot** | Task description only | `"Translate English to French: cat →"` |
| **One-shot** | One example + task | `"cat → chat; dog →"` |
| **Few-shot** | Multiple examples | `"cat → chat; dog → chien; bird →"` |

> **Key Concept:** Larger models make increasingly efficient use of in-context information. This is called "meta-learning" or "learning to learn" — the model learns to adapt from the pattern of examples in the prompt.

### 7.3.4 Scaling Laws

GPT-3 demonstrated that performance improves predictably with:

| Factor | GPT-3 Scale |
|--------|-------------|
| **Model size** | 175 billion parameters |
| **Layers** | 96 |
| **Embedding dim** | 12,288 |
| **Attention heads** | 96 |
| **Training data** | 300 billion tokens |

> **Key Point:** Language modeling performance improves smoothly as model size, dataset size, and compute increase. This predictable scaling is a fundamental property of transformer language models.

### 7.3.5 Training Objective

```
Loss = -Σ_t log P(x_t | x₁, x₂, ..., x_{t-1})
```

Cross-entropy loss over the language modeling task — for each position, predict the actual next token.

## 7.4 Summary: From CNNs to Transformers to LLMs

```
Timeline & Evolution:

1998  LeNet-5        → Handcrafted CNN for digits
2012  AlexNet        → Deep learning breakthrough (GPU + ReLU + Dropout)
2014  VGGNet         → Deeper is better (small filters, many layers)
2015  ResNet         → Skip connections solve degradation
2017  Transformer    → Attention replaces recurrence
2020  ViT            → Pure transformers for vision
2021  CLIP           → Connecting vision and language
2020  GPT-3          → Large-scale in-context learning
```

> **Key Concept:** The field has moved from task-specific architectures with strong inductive biases (CNNs) to general-purpose architectures (Transformers) that learn structure from data at scale. The unifying theme is that **scale + simple architecture + enough data** leads to emergent capabilities.

---

# 8 Practical PyTorch Reference

## 8.1 Essential PyTorch Patterns

### 8.1.1 Model Definition

```python
import torch.nn as nn

class MyModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(1, 32, kernel_size=3, padding=1)
        self.pool = nn.MaxPool2d(2, 2)
        self.fc1 = nn.Linear(32 * 14 * 14, 128)
        self.fc2 = nn.Linear(128, 10)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(0.5)

    def forward(self, x):
        x = self.relu(self.conv1(x))
        x = self.pool(x)
        x = x.view(-1, 32 * 14 * 14)
        x = self.relu(self.fc1(x))
        x = self.dropout(x)
        return self.fc2(x)
```

### 8.1.2 Training Loop Template

```python
import torch.optim as optim

model = MyModel()
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

for epoch in range(num_epochs):
    model.train()
    for inputs, labels in train_loader:
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

    # Validation
    model.eval()
    correct = total = 0
    with torch.no_grad():
        for inputs, labels in val_loader:
            outputs = model(inputs)
            _, predicted = torch.max(outputs, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
    print(f"Epoch {epoch+1}: Accuracy = {100*correct/total:.2f}%")
```

### 8.1.3 Loading Pretrained Models

```python
from torchvision import models

# Load pretrained ResNet
model = models.resnet18(pretrained=True)

# Freeze all layers
for param in model.parameters():
    param.requires_grad = False

# Replace final layer for transfer learning
model.fc = nn.Linear(model.fc.in_features, num_classes)
```

### 8.1.4 Data Augmentation

```python
from torchvision import transforms

train_transform = transforms.Compose([
    transforms.RandomResizedCrop(224),
    transforms.RandomHorizontalFlip(),
    transforms.ColorJitter(brightness=0.2, contrast=0.2),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225])
])
```

## 8.2 Common Loss Functions

| Task | Loss Function | PyTorch |
|------|--------------|---------|
| Regression | MSE | `nn.MSELoss()` |
| Binary classification | Binary Cross-Entropy | `nn.BCELoss()` |
| Multi-class classification | Cross-Entropy | `nn.CrossEntropyLoss()` |
| Image segmentation | BCE / Dice Loss | `nn.BCELoss()` |

## 8.3 Key Hyperparameters

| Hyperparameter | Typical Range | Effect |
|----------------|---------------|--------|
| Learning rate | 1e-5 to 1e-1 | Step size for parameter updates |
| Batch size | 16 to 512 | Samples per gradient update |
| Dropout rate | 0.2 to 0.5 | Fraction of neurons to disable |
| Weight decay | 1e-5 to 1e-3 | L2 regularization strength |
| Number of epochs | 10 to 300+ | Full passes through training data |

> **Best Practice:** Start with standard defaults (Adam, lr=1e-3, batch_size=64) and tune based on validation performance. Use learning rate schedulers (step decay, cosine annealing) for better convergence.



---

# Appendix A: AI for Science Methods

> **Source:** AI + Science (Spring 2026), Dr. Tailin Wu @ Westlake University  
> This appendix covers AI methods specifically developed for or widely applied in scientific discovery, organized by method type and scientific domain.

## A.1 Neural Operators for PDE Simulation

### A.1.1 Motivation: Learning Solution Operators

Traditional numerical solvers solve **one specific instance** of a PDE given fixed initial conditions, boundary conditions, and parameters. Neural operators aim to learn the **solution operator** — a mapping from input functions (e.g., initial state, boundary, parameters) to output functions (the solution field).

```
Traditional Solver:    Given u₀, a, ∂Ω  →  Compute u₁, u₂, ... u_T  (one instance)
Neural Operator:       Learn f_θ: (u₀, a, ∂Ω) → u_T  (generalizes to new instances)
```

> **Key Concept:** Neural operators learn mappings between **infinite-dimensional function spaces**, not just vectors. This allows them to generalize to new PDE instances after training.

### A.1.2 Fourier Neural Operator (FNO)

FNO is a landmark neural operator architecture that operates in the Fourier frequency domain:

```
Input function u(x)
    ↓
Lift to higher dim:  v₀(x) = P(u(x))
    ↓
For each layer l:
    v_{l+1}(x) = σ( W·v_l(x) + F⁻¹(R·F(v_l(x))) )
    │                       │
    │                       └─ Convolution in Fourier space (global integral)
    └─ Local linear transformation
    ↓
Project to output:  u'(x) = Q(v_L(x))
```

**Why Fourier space?**
```
Convolution theorem:  ∫ κ(x-y)·v(y)dy = F⁻¹( F(κ) · F(v) )
```

| Aspect | Advantage | Disadvantage |
|--------|-----------|--------------|
| **Accuracy** | Near state-of-the-art for many PDEs | Requires large training datasets |
| **Resolution** | Can perform **super-resolution** (train on coarse grid, infer on fine grid) | Requires regular grid structure |
| **Speed** | Much faster than classical solvers once trained | — |

> **Key Point:** FNO leverages the convolution theorem — multiplication in Fourier space is equivalent to convolution in physical space, making global integral operations efficient.

### A.1.3 GNN-Based Simulation

For systems naturally represented as graphs (particles, meshes, molecules), Graph Neural Networks (GNNs) are the architecture of choice:

**Generic GNN Message Passing:**
```
For each node i:
    1. Compute messages on edges:    m_{j→i} = MLP_msg(n_j, n_i, e_ji)
    2. Accumulate messages:          M_i = Σ_{j∈N(i)} m_{j→i}
    3. Update node features:         n_i' = MLP_update(n_i, M_i)
```

**Key GNN Simulators:**

| Model | Year | Contribution | Application |
|-------|------|--------------|-------------|
| **GNS** | ICML 2020 | First general GNN simulator | Particle-based systems |
| **MeshGraphNets** | ICLR 2021 | Mesh-space + world-space edges; remeshing | Deformable objects, fluids |
| **LAMP** | KDD 2022 | Large-scale subsurface simulation | Carbon capture, energy |
| **HGNS** | ICLR 2023 | Multi-resolution, sector-based inference | 10M cells per step |
| **GraphCast** | Science 2023 | Multi-scale GNN for weather | 10-day global forecasting |

> **Key Concept:** Symmetry-aware GNNs (e.g., E(n)-equivariant GNNs) enforce physical symmetries (translation, rotation, permutation) inductive biases, leading to better generalization and data efficiency.

### A.1.4 Inverse Design with Differentiable Simulators

Once a neural surrogate model is trained, we can use **backpropagation through time** to optimize design/control variables:

```
Training:    Learn f_θ: (u_t, a, ∂Ω) → u_{t+1}
Inference:   Optimize ∂Ω to maximize L(u_[0:T])
             via ∇_{∂Ω} L = backprop through simulation rollout
```

| Approach | Method | Example |
|----------|--------|---------|
| **Surrogate + Gradient** | Backprop through learned simulator | Airfoil shape optimization (minimize drag) |
| **Reinforcement Learning** | Policy gradient for sequential control | Tokamak plasma control |
| **Diffusion Models** | Score-based generative design | Material crystal structure generation |

## A.2 Symbolic Regression

### A.2.1 Problem Definition

> **Key Concept:** Symbolic Regression discovers **exact, interpretable mathematical expressions** from data, as opposed to black-box neural network approximations.

**Given:** Dataset D = {(x_i, y_i)} where x_i ∈ ℝ^d, y_i ∈ ℝ  
**Find:** f* = argmin_{f∈F} L(f) where F is a function class of symbolic compositions (exp, sin, log, +, ×, etc.)

### A.2.2 Methods

| Method | Approach | Search Space |
|--------|----------|--------------|
| **Linear SR** | Linear combination of basis functions | Coefficients θ ∈ ℝ^n |
| **Neural SR** | MLP with symbolic activation functions | Weights W, biases b |
| **Expression-tree Search** | Genetic programming | Tree structures |
| **Transformer-based** | set2seq mapping | Sequence of tokens |
| **RL-based** | Policy gradient for tree generation | Policy π(a\|s) |
| **Physics-inspired (AI Feynman)** | Physical dimension constraints + modular search | Physics-guided expression space |

### A.2.3 AI Feynman

AI Feynman uses physics-inspired constraints to dramatically reduce the search space:

1. **Dimensional analysis:** Only combine terms with matching physical units
2. **Graph modularity:** Decompose complex equations into simpler subgraphs
3. **Pareto optimality:** Balance complexity vs. accuracy

> **Key Result:** AI Feynman 2.0 rediscovered 100 top physics equations from the Feynman Lectures. Other systems discovered conservation laws from trajectory data and re-discovered heliocentrism from solar system observations.

## A.3 Reinforcement Learning for Scientific Control

### A.3.1 RL Basics for Science

Scientific control problems are naturally formulated as Markov Decision Processes (MDP):

| Component | Scientific Control Example |
|-----------|---------------------------|
| **State s** | Plasma probe signals, fluid velocity field, molecular configuration |
| **Action a** | Coil voltages, valve openings, reaction conditions |
| **Reward r** | Target shape match, energy efficiency, reaction yield |
| **Policy π(a\|s)** | Controller mapping observations to actions |

**Objective:** Maximize expected cumulative reward
```
max_π 𝔼[Σ_t γ^t · r_t]
```

### A.3.2 Case Study: Plasma Configuration Control

**Problem:** Control 19 magnetic coils in a tokamak to shape and maintain high-temperature plasma.

| Aspect | Detail |
|--------|--------|
| **State** | Probe signals s ∈ ℝ^n (10 kHz sampling) |
| **Action** | Coil voltages a ∈ ℝ^19 |
| **Control target** | Time-varying plasma current and boundary shape g ∈ ℝ^m |
| **Policy** | π(a \| s, g) — conditions on target shape |
| **RL algorithm** | MPO (Maximum a Posteriori Policy Optimization) |
| **Architecture** | Actor: small MLP (must run at 10 kHz); Critic: LSTM (training only) |

> **Key Result:** DeepMind's RL controller (Nature 2022) achieved real-time plasma control and discovered novel plasma configurations previously considered infeasible.

### A.3.3 Key RL Algorithms for Science

| Algorithm | Update Rule | Best For |
|-----------|-------------|----------|
| **SARSA** | On-policy TD: q ← q + α[r + γq(s',a') - q(s,a)] | Stable environments |
| **Q-Learning** | Off-policy: q ← q + α[r + γ max_a q(s',a) - q(s,a)] | Exploration-heavy tasks |
| **n-step SARSA** | Multi-step returns for lower bias | Long-horizon control |
| **Monte Carlo** | Full episode returns | Episodic scientific experiments |

## A.4 Foundation Models for Science

### A.4.1 What is a Scientific Foundation Model?

> **Key Concept:** A foundation model is trained on diverse scientific tasks/data and can generalize to new tasks with minimal or no task-specific training.

```
Task 1:  Input X⁽¹⁾ → Target Y⁽¹⁾
Task 2:  Input X⁽²⁾ → Target Y⁽²⁾
   ...
Task n:  Input X⁽ⁿ⁾ → Target Y⁽ⁿ⁾
           ↓
    Single foundation model f_θ
```

### A.4.2 Key Examples

| Model | Domain | Approach | Impact |
|-------|--------|----------|--------|
| **AlphaFold 2/3** | Protein structures | Evoformer + IPA / Diffusion module | Predicted 200M+ protein structures |
| **Uni-Mol** | Molecular representation | Universal 3D molecular learning | General molecular property prediction |
| **GET** | Gene expression | Foundation model across cell types | Predicts transcription in unseen cell types |
| **LeanDojo** | Theorem proving | LLM + retrieval-augmented generation | Formal mathematics in Lean |
| **AlphaGeometry** | Geometry | Neuro-symbolic + synthetic data | Solves IMO geometry problems |

### A.4.3 LLM for Theorem Proving

**LeanDojo Pipeline:**
1. Extract formal proof data from Lean mathematical library
2. Train retrieval-augmented language model
3. Interact with Lean proof environment for step-by-step generation

> **Recent Result (2026):** A single mathematician supervised an AI-assisted formalization of the Vlasov-Maxwell-Landau equilibrium proof in 10 days at $200 cost — the AI reasoning model generated the proof, agentic coding translated it to Lean, and a specialized prover closed 111 lemmas.

## A.5 Diffusion Models for Science

### A.5.1 Core Idea

Diffusion models learn to reverse a gradual noising process:

```
Forward (training):   x₀ → x₁ → x₂ → ... → x_T  (add Gaussian noise)
Reverse (sampling):   x_T → ... → x₂ → x₁ → x₀  (learned denoising)
```

**Training objective:** Given noisy data x_t at step t, predict the noise ε that was added:
```
L = 𝔼_{x₀, t, ε} || ε_θ(x_t, t) - ε ||²
```

### A.5.2 Scientific Applications

| Application | Model | Task |
|-------------|-------|------|
| **Protein design** | RFDiffusion | Generate novel protein backbones and sequences |
| **Material design** | CDVAE / DiffCSP | Generate stable crystal structures |
| **Molecule generation** | GeoDiff, DiGress | 3D molecular conformer generation |
| **Flow reconstruction** | Physics-informed diffusion | High-fidelity fluid field reconstruction |

### A.5.3 RFDiffusion for Protein Design

RFDiffusion adapts diffusion models to the protein structure domain:

**Training:** Denoise protein structures from Gaussian noise in 3D coordinate space  
**Conditional generation:** Design proteins given:
- Partial sequence constraints
- Binding target structure
- Functional motif coordinates
- Fold topology specifications

> **Key Concept:** Diffusion models for science are not just generative — they can be used for **inverse design** by conditioning on desired functional properties.

## A.6 Multi-Agent Systems for Scientific Research

### A.6.1 AI Agents for Science

Scientific research involves iterative cycles of hypothesis, experiment, analysis, and refinement — well-suited to agentic AI:

```
Hypothesis Agent → Experiment Agent → Analysis Agent → Refinement Agent
        ↑___________________________________________________|
```

### A.6.2 Key Frameworks and Applications

| Framework | Purpose |
|-----------|---------|
| **AutoGen (Microsoft)** | Multi-agent conversation and collaboration |
| **MetaGPT** | Software development with role-based agents |
| **AI Co-Scientist (Google)** | Virtual scientific collaborator for hypothesis generation |
| **Autonomous Labs** | Self-driving experimental platforms |

**Case Study: Self-Driving Protein Lab**
- AI designs protein variants predicted to improve fitness
- Robotic lab automatically synthesizes and tests them
- Results feed back to AI for next iteration
- Discovered novel proteins with improved properties

---

# Appendix B: AI for Life Science

## B.1 Protein Structure Prediction

### B.1.1 The Protein Folding Problem

**Input:** Amino acid sequence (20 types, typically 100-1000 residues)  
**Output:** 3D coordinates of all heavy atoms (N, Cα, C, O, side chains)

> **Key Point:** This is one of biology's grand challenges. Experimental methods (X-ray crystallography, cryo-EM) have determined ~100,000 structures, but there are billions of known protein sequences.

**Why it's hard:**
- **Combinatorial complexity:** Astronomical number of possible conformations
- **Rugged energy landscape:** Many local minima trap optimization methods
- **Dynamic regions:** Intrinsically disordered regions lack fixed structure

### B.1.2 AlphaFold 2

AlphaFold 2 (DeepMind, Nature 2021) achieved near-experimental accuracy:

| Metric | AlphaFold 2 | Next Best Method |
|--------|-------------|-----------------|
| RMSD@95 (CASP14) | 0.96 Å | 2.8 Å |

**Key Architecture Components:**

| Module | Function |
|--------|----------|
| **MSA (Multiple Sequence Alignment)** | Evolutionary co-variation statistics from homologous sequences |
| **Evoformer** | Transformer blocks operating on both MSA and pair representations |
| **IPA (Invariant Point Attention)** | Attention mechanism in 3D space for structure refinement |
| **Structure Module** | Iterative refinement of atomic coordinates |

> **Key Result:** AlphaFold 2 predicted structures for over 200 million proteins across ~1 million species — essentially covering every known protein on Earth.

### B.1.3 AlphaFold 3

AlphaFold 3 (Nature 2024) extends prediction to **biomolecular interactions**:

```
AlphaFold 2:  Protein sequence → Protein structure
AlphaFold 3:  Joint structure prediction of:
              • Protein + DNA/RNA complexes
              • Protein + small molecule (drug) binding
              • Protein + ion/modified residue interactions
```

**Architecture change:** Replaced IPA with a **diffusion module** for joint structure generation.

## B.2 Protein Design

### B.2.1 Problem Formulation

| Type | Formulation |
|------|-------------|
| **Unconditional design** | Generate new protein structures: X ∼ p(X) |
| **Conditional design** | Generate structure given constraints: X ∼ p(X \| condition) |

**Conditions include:** partial sequence, binding target, fold type, functional motif coordinates.

### B.2.2 RFDiffusion

RFDiffusion (Baker Lab) uses a diffusion model trained on protein structures:

```
Training:   Learn to denoise protein backbone coordinates from Gaussian noise
Inference:  Start from random noise → Iteratively denoise → Valid protein structure
```

**Capabilities:**
- De novo protein design (no template needed)
- Binder design (proteins that bind specific targets)
- Symmetric oligomer design
- Motif scaffolding (build structure around functional motifs)

## B.3 Gene Perturbation Prediction

### B.3.1 The Challenge

> **Key Concept:** Predicting how a cell responds to genetic perturbations is fundamental to understanding gene function and designing therapies.

**Combinatorial explosion:**
- ~20,000 single-gene perturbations
- ~40 million double-gene perturbations
- ~160 billion triple-gene perturbations

**Question:** Can we predict transcriptional outcomes of gene combinations never seen experimentally?

### B.3.2 GEARS: Graph-Based Perturbation Prediction

GEARS (Nature Biotechnology 2024) uses GNNs with biological inductive biases:

| Inductive Bias | Implementation |
|----------------|----------------|
| **Gene relationships** | Gene co-expression graph |
| **Perturbation relationships** | Perturbation interaction graph |
| **Cross-gene information** | GNN message passing across both graphs |

> **Key Result:** GEARS accurately predicts outcomes of novel multigene perturbations, including non-additive interactions (synergy/antagonism) that simple linear models miss.

### B.3.3 GET: Foundation Model for Transcription

GET (Nature 2025) is a foundation model trained across diverse human cell types:

- **Input:** DNA sequence + cell type context
- **Output:** Gene expression levels
- **Capability:** Achieves experimental-level accuracy even for **previously unseen cell types**
- **Discovery:** Uncovers universal and cell-type-specific transcription factor interaction networks

## B.4 Spatial Omics

### B.4.1 What is Spatial Omics?

Spatial omics measures biological molecules (RNA, proteins, metabolites) **in their native spatial locations** within tissues, preserving spatial context lost in bulk sequencing.

| Technology | Approach | Resolution | Gene Coverage |
|------------|----------|------------|---------------|
| **Visium HD** | Sequencing-based | Subcellular | Full transcriptome |
| **MERFISH** | Imaging-based | Single-cell | ~10,000 genes |
| **CosMx** | Imaging-based | Single-cell | ~1,000 genes |

### B.4.2 AI for Spatial Omics

**Challenge:** No single technology captures both full genomic coverage and single-cell spatial resolution.

**AI Solution:** Train models to infer unobserved modalities:
```
Input:  Spatial transcriptomics (low-res or partial genes)
Output: Single-cell resolution + full transcriptome + protein levels
```

**Applications:**
- **Tumor microenvironment analysis:** Identify tumor/stromal/immune cell interactions
- **3D tissue reconstruction:** Stack 2D slices into 3D with AI alignment
- **Personalized medicine:** Match treatments to spatial molecular signatures

## B.5 Drug Discovery

### B.5.1 AI in the Drug Discovery Pipeline

| Stage | Traditional Challenge | AI Solution |
|-------|----------------------|-------------|
| **Target identification** | Slow hypothesis generation | Foundation models for gene-disease links |
| **Hit discovery** | Random screening | Generative models for novel molecular structures |
| **Lead optimization** | Many synthesis cycles | Predictive models for ADMET properties |
| **Clinical prediction** | High failure rates | AI for biomarker and patient stratification |

### B.5.2 Autonomous Drug Discovery Platforms

**LUMI-lab (Cell 2026):** A foundation model-driven autonomous platform for ionizable lipid design:

```
Foundation Model predicts lipid properties
    ↓
Generative model proposes novel designs
    ↓
Automated synthesis and testing
    ↓
Results feedback for model refinement
```

### B.5.3 The Virtual Cell Vision

> **Key Concept:** The ultimate goal is an **AI Virtual Cell (AIVC)** — a comprehensive computational model that can simulate cellular behavior across contexts, predict responses to perturbations, and guide experimental design.

**Grand Challenges:**
- Establishing self-consistency across different data types and scales
- Balancing interpretability with biological utility
- Ensuring ethical and responsible use
- Prioritizing large-scale data generation for under-studied contexts

