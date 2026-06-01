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

## 7.5 LLM Foundations: Pre-training and SFT

Large language models are trained in two main stages: **pre-training** learns general language patterns from raw text, and **supervised fine-tuning (SFT)** aligns the model to follow instructions.

### 7.5.1 Pre-training: Next-Token Prediction

Pre-training is **self-supervised**: no human labels are required. The training target is simply the next token already present in the text.

**Objective:**
```
P(w₁, ..., wₙ) = ∏ P(wₜ | w₁, ..., wₜ₋₁)
```

The model learns to complete text one token at a time by minimizing cross-entropy loss against the true next token.

**Common corpora:**
| Source | Content |
|--------|---------|
| Wikipedia | Encyclopedic articles |
| BookCorpus | Published books |
| Common Crawl | Web pages |
| GitHub | Code repositories (for code-capable models) |

> **Key Concept:** Pre-training teaches **fluent continuation**, not task behavior. Instruction tuning later bridges this gap.

### 7.5.2 Supervised Fine-Tuning (SFT)

After pre-training, the model is fine-tuned on labeled (input, output) pairs to align it with specific tasks.

| Stage | Data | Goal |
|-------|------|------|
| **Pre-training** | Raw text | Learn grammar, semantics, world knowledge |
| **SFT** | (instruction, response) pairs | Teach task-following behavior |

```
input x  →  model  →  prediction
                    ↓
                  target y
                    ↓
            minimize loss(prediction, y)
```

Examples of SFT tasks:
- Sentiment classification: sentence → positive/negative
- Question answering: question → answer
- Code generation: description → code snippet

## 7.6 Visual Instruction Tuning: LLaVA

### 7.6.1 Motivation

Text-only LLMs benefit from instruction tuning, but multimodal tasks lack scalable vision-language instruction datasets. **LLaVA** (Liu et al., 2023) proposes a lightweight paradigm for turning a frozen LLM into a visual assistant.

### 7.6.2 Architecture

```
Image  →  CLIP ViT-L/14  →  Linear Projector  →  Vicuna LLM  →  Response
         (vision encoder)      (W · Z)            (frozen)
```

A single projection matrix maps visual features into the same token space the LLM already understands. The LLM itself remains frozen — only the projector is trained.

| Component | Role |
|-----------|------|
| **Vision Encoder** | CLIP ViT extracts image features |
| **Linear Projector** | Maps visual tokens to language embedding space |
| **LLM** | Frozen language model (e.g., Vicuna) generates text |

### 7.6.3 Two-Stage Training

| Stage | What is trained | Goal |
|-------|----------------|------|
| **1. Alignment** | Only the projection matrix | Align visual features to LLM token space |
| **2. Behavior tuning** | Projection + LLM LoRA layers | Teach multi-turn dialogue and instruction following |

> **Key Point:** Separating alignment from behavior learning keeps the architecture simple and makes the data contribution legible.

## 7.7 Image Generation with Diffusion Models

### 7.7.1 Stable Diffusion Overview

Stable Diffusion generates images by iteratively **denoising** a random latent tensor. The core idea: start from pure noise, then gradually refine it into a coherent image guided by a text prompt.

**Key components:**
- **VAE**: Compresses images into a lower-dimensional latent space
- **U-Net**: Predicts noise to remove at each step
- **Text Encoder (CLIP)**: Converts prompts into conditioning vectors
- **Scheduler**: Controls the denoising trajectory

### 7.7.2 Cross-Attention: Where Text Meets Image

Inside the U-Net, **cross-attention layers** inject text conditioning into the image generation process:

```
Query: image features from U-Net
Key/Value: text embeddings from CLIP

Output: image features influenced by text semantics
```

This is how "a cat wearing a hat" influences the pixels being generated.

### 7.7.3 Controllable Generation

| Method | Mechanism | Use Case |
|--------|-----------|----------|
| **ControlNet** | Duplicate U-Net layers, train on edge/pose/depth maps | Control composition without retraining base model |
| **IP-Adapter** | Learn image prompt embeddings via decoupled cross-attention | Transfer style/content from reference images |

> **Key Concept:** ControlNet and IP-Adapter add controllability **without modifying the base diffusion model**, making them lightweight and composable.

## 7.8 Practice: ComfyUI Workflows

ComfyUI represents image generation as a **node graph** — each node performs one operation, and edges define data flow. This makes experiments reproducible and workflows shareable.

### 7.8.1 The Six Core Nodes

Every text-to-image workflow uses these six node families:

| # | Node | Function |
|---|------|----------|
| 1 | **Load Checkpoint** | Loads the base model (UNet + CLIP + VAE) |
| 2 | **CLIP Text Encode** | Converts positive/negative prompts into conditioning vectors |
| 3 | **Empty Latent** | Sets canvas size (width, height, batch size) |
| 4 | **KSampler** | Runs the iterative denoising loop |
| 5 | **VAE Decode** | Converts final latent tensor back into pixels |
| 6 | **Save Image** | Writes the result to a PNG file |

### 7.8.2 KSampler Parameters

| Parameter | Meaning | Typical Value |
|-----------|---------|---------------|
| **seed** | Random seed for reproducibility | fixed or random |
| **steps** | Number of denoising iterations | 20-50 |
| **cfg** | How strongly to follow the prompt | 7-8 |
| **sampler** | Noise trajectory algorithm | euler_a, dpmpp_2m |
| **denoise** | How much to change the latent | 1.0 (full generation) |

> **Key Concept:** Once these six nodes make sense, most larger workflows (inpainting, img2img, ControlNet) stop looking mysterious — they are just additional nodes plugged into the same graph.

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

# 9 Diffusion Models: From DDPM to Latent Diffusion

> **Source:** SCI 1003 Class 9, Dr. Chi Zhang @ Westlake AGI Lab  
> Diffusion models are a family of generative models that learn to reverse a gradual noising process. This chapter covers the mathematical foundations of DDPM, the efficiency gains of Latent Diffusion Models, and the practical mechanism of Classifier-Free Guidance.

## 9.1 What Are Diffusion Models?

Diffusion models are inspired by **non-equilibrium thermodynamics**. They define a Markov chain of diffusion steps that slowly add random noise to data, then learn to reverse this process to construct desired data samples from noise.

| Model Family | Year | Key Idea |
|--------------|------|----------|
| **Diffusion Probabilistic Models** | 2015 | Forward noising + reverse denoising as Markov chain |
| **NCSN** (Noise-Conditioned Score Network) | 2019 | Learn score function (gradient of log data density) |
| **DDPM** (Denoising Diffusion Probabilistic Models) | 2020 | Simplified training; predicts noise directly |

> **Key Concept:** Diffusion models consist of two processes: a **forward diffusion process** that adds noise, and a **reverse diffusion process** that removes it. The model learns the reverse process.

## 9.2 Forward Diffusion Process

Given a data sample $x_0 \sim q(x)$, the forward process adds small amounts of Gaussian noise over $T$ steps, producing a sequence $x_1, x_2, ..., x_T$.

**Step sizes are controlled by a variance schedule** $\{\beta_t \in (0,1)\}_{t=1}^T$:

$$q(x_t | x_{t-1}) = \mathcal{N}(x_t; \sqrt{1 - \beta_t} \, x_{t-1}, \beta_t \mathbf{I})$$

### 9.2.1 Closed-Form Expression

A key insight: we can sample $x_t$ directly from $x_0$ without iterating through all intermediate steps. Define:

$$\alpha_t = 1 - \beta_t, \quad \bar{\alpha}_t = \prod_{s=1}^t \alpha_s$$

Then:

$$q(x_t | x_0) = \mathcal{N}(x_t; \sqrt{\bar{\alpha}_t} \, x_0, (1 - \bar{\alpha}_t) \mathbf{I})$$

Or equivalently:

$$x_t = \sqrt{\bar{\alpha}_t} \, x_0 + \sqrt{1 - \bar{\alpha}_t} \, \epsilon, \quad \text{where } \epsilon \sim \mathcal{N}(0, \mathbf{I})$$

> **Key Point:** As $t \to \infty$, $x_T$ becomes pure isotropic Gaussian noise. The data sample gradually loses all distinguishable features.

## 9.3 Reverse Diffusion Process

If we could reverse the forward process and sample from $q(x_{t-1} | x_t)$, we could generate data from pure noise $x_T \sim \mathcal{N}(0, \mathbf{I})$.

Unfortunately, $q(x_{t-1} | x_t)$ is intractable. We therefore learn a model $p_\theta$ to approximate these conditional probabilities:

$$p_\theta(x_{t-1} | x_t) = \mathcal{N}(x_{t-1}; \mu_\theta(x_t, t), \Sigma_\theta(x_t, t))$$

### 9.3.1 The Training Objective

DDPM simplifies the problem by training a neural network to **predict the noise** $\epsilon$ that was added:

$$\mathcal{L}_{\text{DDPM}} = \mathbb{E}_{x_0, t, \epsilon} \left[ \| \epsilon - \epsilon_\theta(x_t, t) \|^2 \right]$$

Where:
- $x_t$ is created via the forward process from clean data $x_0$
- $t$ is sampled uniformly from $\{1, ..., T\}$
- $\epsilon \sim \mathcal{N}(0, \mathbf{I})$ is the noise we want the model to predict

> **Key Concept:** Instead of predicting the denoised image directly, the model predicts the **noise residual**. This is mathematically equivalent but empirically more stable.

### 9.3.2 Sampling (Reverse Process)

At inference time, we start from $x_T \sim \mathcal{N}(0, \mathbf{I})$ and iteratively denoise:

$$x_{t-1} = \frac{1}{\sqrt{\alpha_t}} \left( x_t - \frac{1 - \alpha_t}{\sqrt{1 - \bar{\alpha}_t}} \, \epsilon_\theta(x_t, t) \right) + \sigma_t z$$

Where $z \sim \mathcal{N}(0, \mathbf{I})$ (only when $t > 1$).

## 9.4 Denoising Diffusion Probabilistic Models (DDPM)

### 9.4.1 Noise Schedule

A common choice is a **linear schedule**:

$$\beta_t = \text{linspace}(\beta_{\text{start}}, \beta_{\text{end}}, T)$$

| Parameter | Typical Value | Description |
|-----------|---------------|-------------|
| $T$ | 1000-2000 | Number of diffusion steps |
| $\beta_{\text{start}}$ | $10^{-4}$ | Initial noise level |
| $\beta_{\text{end}}$ | 0.02 | Final noise level |

### 9.4.2 Precomputed Terms

For efficient training and sampling, precompute:

```
alphas      = 1.0 - betas
alphas_cumprod = cumprod(alphas)
sqrt_alphas_cumprod = sqrt(alphas_cumprod)
sqrt_one_minus_alphas_cumprod = sqrt(1 - alphas_cumprod)
```

## 9.5 Latent Diffusion Model (LDM)

> **Core Thesis:** Spend diffusion capacity on semantics, not on nearly invisible pixel detail.

### 9.5.1 Motivation

Pixel-space diffusion is expensive: every bit of the image participates in the diffusion process, yet most bits contribute only to perceptual details. The semantic and conceptual composition remains stable even after aggressive compression.

**LDM = DDPM + VAE**

| Stage | Operation | Purpose |
|-------|-----------|---------|
| **Stage A: Autoencoder** | Encode pixels → latents; Decode latents → pixels | Remove perceptual redundancy once |
| **Stage B: Diffusion** | Predict noise in latent space | Focus on semantic composition |
| **Stage C: Conditioning** | Cross-attention with text/boxes/maps | Control generation flexibly |
| **Stage D: Decode** | VAE decoder reconstructs pixels | Final image output |

### 9.5.2 Architecture

```
Pixels x          Condition y (text / boxes / maps)
    │                      │
    ▼                      ▼
Encoder E          Condition encoder τ_θ
    │                      │
    ▼                      ▼
Latent z  ──────→  U-Net denoiser ←── Cross-Attention (Q from UNet, K/V from τ_θ)
    │                      │
    ▼                      ▼
Decoder D          Denoised latent z_0
    │
    ▼
Reconstructed image
```

**Training objective in latent space:**

$$\mathcal{L}_{\text{LDM}} = \mathbb{E}_{z_0, t, \epsilon, y} \left[ \| \epsilon - \epsilon_\theta(z_t, t, \tau_\theta(y)) \|^2 \right]$$

Where $z_0 = E(x)$ is the encoded latent.

### 9.5.3 Compression Factor

The paper studies downsampling factors $f \in \{2, 4, 8, 16, 32\}$:

| Factor | Quality | Speed | Verdict |
|--------|---------|-------|---------|
| $f = 1$–$2$ | Excellent | Slow | Too expensive |
| $f = 4$–$8$ | Best balance | Fast | **Sweet spot** |
| $f = 32$ | Degraded | Fastest | Too lossy |

> **Key Point:** A 38-point FID gap separates LDM-1 (no compression) from LDM-8 after 2M training steps. Moderate compression is the sweet spot.

### 9.5.4 Cross-Attention for Conditioning

Cross-attention layers inside the U-Net inject text (or other modalities) into the generation process:

- **Query (Q):** from U-Net image features
- **Key (K) / Value (V):** from condition encoder $\tau_\theta(y)$

This generalizes beyond text-to-image: boxes, semantic maps, and depth images can all be encoded as conditioning tokens.

## 9.6 Classifier-Free Guidance (CFG)

### 9.6.1 The Problem

A direct conditional model gives one answer per prompt. There is no knob to trade off **fidelity** (how closely the image matches the prompt) against **diversity** (how varied the outputs are).

### 9.6.2 The Idea

Train **one denoiser** to work in two modes: with the condition and without it. At test time, compare the two outputs and push the sample toward the prompt.

**Training rule:**

```
c_train = c            with probability 1 - p_uncond
c_train = empty        with probability p_uncond
loss = || ε_θ(z, c_train) - ε ||²
```

> **Key Concept:** During training, randomly drop the condition (replace with empty/null) some fraction of the time. The same model learns both conditional and unconditional denoising.

### 9.6.3 Sampling Rule

At each denoising step, compute both the conditional and unconditional noise estimates, then extrapolate:

$$\epsilon_{\text{guided}} = (1 + w) \cdot \epsilon_{\text{cond}} - w \cdot \epsilon_{\text{uncond}}$$

Or equivalently:

$$\epsilon_{\text{guided}} = \epsilon_{\text{uncond}} + s \cdot (\epsilon_{\text{cond}} - \epsilon_{\text{uncond}})$$

Where:
- $w$ = extra guidance strength
- $s = 1 + w$ (common implementation)

| Guidance Scale | Effect |
|----------------|--------|
| $s = 1$ ($w = 0$) | No guidance; diverse but less faithful |
| $s = 7$–$8$ | Typical default; good balance |
| $s > 15$ | Very faithful but often oversaturated/artifacted |

> **Best Practice:** CFG is the standard mechanism for controlling prompt adherence in Stable Diffusion and related models. It requires no additional model training at inference time.

## 9.7 Practice: DDPM Toy Example

The course provides a minimal DDPM implementation on the 2D Swiss Roll dataset. The code demonstrates all core concepts: forward noising, noise prediction training, and iterative sampling.

```python
import math
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from sklearn.datasets import make_swiss_roll

# ---------- 1. Data ----------
def sample_swiss_roll(n_samples=1000, noise=0.25):
    data, _ = make_swiss_roll(n_samples, noise=noise)
    data = data[:, [0, 2]]  # keep x and z
    stdev = np.sqrt((39 * math.pi ** 2 / 8 - 4) + np.array([[-1, 1]]) * 0.25 + noise ** 2)
    data = data / stdev
    return torch.tensor(data, dtype=torch.float32)

# ---------- 2. Model ----------
class MLP(nn.Module):
    def __init__(self, dim):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(dim + 1, 128), nn.ReLU(),
            nn.Linear(128, 128), nn.ReLU(),
            nn.Linear(128, dim),
        )

    def forward(self, x, t):
        t = t.unsqueeze(1) / 1000.0
        x_input = torch.cat([x, t], dim=1)
        return self.net(x_input)

# ---------- 3. Diffusion Schedule ----------
T = 2000
betas = torch.linspace(1e-4, 0.02, T)
alphas = 1.0 - betas
alphas_cumprod = torch.cumprod(alphas, dim=0)
sqrt_alphas_cumprod = torch.sqrt(alphas_cumprod)
sqrt_one_minus_alphas_cumprod = torch.sqrt(1 - alphas_cumprod)

# ---------- 4. Forward Process ----------
def q_sample(x_start, t, noise=None):
    if noise is None:
        noise = torch.randn_like(x_start)
    return (sqrt_alphas_cumprod[t].view(-1, 1) * x_start
            + sqrt_one_minus_alphas_cumprod[t].view(-1, 1) * noise)

# ---------- 5. Training Loop ----------
def train(model, data, epochs=1000, batch_size=128, lr=1e-3):
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    n = len(data)
    for epoch in range(epochs):
        idx = torch.randperm(n)
        data_shuffled = data[idx]
        for i in range(0, n, batch_size):
            x = data_shuffled[i:i + batch_size]
            t = torch.randint(0, T, (x.size(0),))
            noise = torch.randn_like(x)
            x_t = q_sample(x, t, noise)
            pred = model(x_t, t.float())
            loss = F.mse_loss(pred, noise)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
        if (epoch + 1) % 100 == 0:
            print(f"Epoch {epoch + 1}: loss = {loss.item():.4f}")

# ---------- 6. Sampling (Reverse Process) ----------
@torch.no_grad()
def p_sample_loop(model, shape):
    x = torch.randn(shape)
    for t in reversed(range(T)):
        t_batch = torch.full((shape[0],), t, dtype=torch.float)
        noise_pred = model(x, t_batch)
        beta_t = betas[t]
        sqrt_one_minus_alpha = sqrt_one_minus_alphas_cumprod[t]
        sqrt_recip_alpha = 1.0 / torch.sqrt(alphas[t])
        x = sqrt_recip_alpha * (x - beta_t / sqrt_one_minus_alpha * noise_pred)
        if t > 0:
            x += torch.sqrt(beta_t) * torch.randn_like(x)
    return x

# ---------- 7. Run ----------
if __name__ == "__main__":
    torch.manual_seed(0)
    data = sample_swiss_roll(1000, noise=0.25)
    model = MLP(dim=2)
    train(model, data, epochs=5000)
    samples = p_sample_loop(model, (1000, 2))
    # Compare real vs generated with matplotlib
```

> **Key Concept:** This toy example shows that diffusion works on any data modality, not just images. The same mathematics applies to 2D points, images, audio, or protein structures.

## 9.8 Timeline of Diffusion-Based Image Generation

| Year | Milestone | Significance |
|------|-----------|--------------|
| 2015.06 | Diffusion Probabilistic Models (Sohl-Dickstein et al.) | First diffusion framework |
| 2019 | NCSN (Song & Ermon) | Score-based perspective |
| 2020.06 | DDPM (Ho et al.) | Simplified training; high-quality samples |
| 2021.12 | LDM (Rombach et al.) | Latent space diffusion; text conditioning |
| 2022.08 | Stable Diffusion v1 | Open-source text-to-image |
| 2022.10 | SD v1.5 | Improved quality |
| 2023.06 | SDXL | Larger U-Net; better text rendering |
| 2024.03 | SD3 | New architecture (MMDiT) |

---

# 10 LLM Adaptation, Multimodal AI, and Controllable Generation

> **Source:** SCI 1003 Class 10, Dr. Chi Zhang @ Westlake AGI Lab  
> This chapter bridges three domains: adapting LLMs through instruction tuning, building multimodal assistants, and controlling image generation with diffusion models.

## 10.1 LLM Foundations: Pre-training and Adaptation

### 10.1.1 Pre-training: Next-Token Prediction

Pre-training is **self-supervised**: no human labels are required. The training target is the next token already present in the text.

$$P(w_1, ..., w_n) = \prod_{t} P(w_t \mid w_1, ..., w_{t-1})$$

**Common corpora:**

| Source | Content |
|--------|---------|
| Wikipedia | Encyclopedic articles |
| BookCorpus | Published books |
| Common Crawl | Web pages |
| GitHub | Code repositories |

> **Key Concept:** Pre-training teaches **fluent continuation**, not task behavior. Instruction tuning later bridges this gap.

### 10.1.2 Supervised Fine-Tuning (SFT)

After pre-training, the model is fine-tuned on labeled (input, output) pairs:

| Stage | Data | Goal |
|-------|------|------|
| **Pre-training** | Raw text | Learn grammar, semantics, world knowledge |
| **SFT** | (instruction, response) pairs | Teach task-following behavior |

```
input x  →  model  →  prediction
                    ↓
                  target y
                    ↓
            minimize loss(prediction, y)
```

> **Key Point:** The full pipeline is: Pre-training → SFT → RLHF (optional). Each stage builds on the previous without replacing it.

## 10.2 Visual Instruction Tuning: LLaVA

### 10.2.1 The Bottleneck

Text-only LLMs benefit from instruction tuning, but multimodal tasks lacked scalable vision-language instruction datasets. The key question: **how do we cheaply create instruction-following data for images?**

| What Existed | What Was Missing |
|--------------|------------------|
| Images paired with captions | Multi-turn instruction-following data |
| Vision models specialized by task | Rich answers beyond one-sentence captions |
| Systems that describe what they see | Benchmarks for useful assistant behavior |

### 10.2.2 Data Engine: GPT-4 as a Teacher

LLaVA reframes the shortage of multimodal instructions as a **data reformation problem**:

```
Existing corpora (captions + bounding boxes)
        ↓
Prompt GPT-4 with textual proxies of the image
        ↓
Generate: conversation · detailed description · complex reasoning
        ↓
Instruction-tune visual assistant
```

> **Key Point:** GPT-4 never sees the image itself during data generation; it sees **textual proxies** (captions + bounding boxes). This makes data synthesis cheaper and scalable, but makes caption quality absolutely central.

**Dataset composition:**

| Type | Size | Purpose |
|------|------|---------|
| Conversation | 58K | Multi-turn QA grounded in visible content |
| Detailed description | 23K | Dense scene narration |
| Complex reasoning | 77K | Logic beyond literal description |
| **Total** | **158K** | Unique language-image instruction samples |

### 10.2.3 Architecture

```
Image → CLIP ViT-L/14 → Linear Projector W → Vicuna LLM → Response
         (vision encoder)   (H_v = W · Z_v)   (frozen)
```

A single projection matrix maps visual features into the same token space the LLM already knows how to process. This is the **minimum interface** needed to let a frozen LLM consume visual evidence.

| Component | Role |
|-----------|------|
| **Vision Encoder** | CLIP ViT extracts image features |
| **Linear Projector** | Maps visual tokens to language embedding space |
| **LLM** | Frozen language model generates text |

> **Key Concept:** The paper is architecture-light because it wants the **data contribution** to be legible. Simple interfaces are enough when the data is right.

### 10.2.4 Two-Stage Training

| Stage | What Is Trained | Data | Goal |
|-------|----------------|------|------|
| **1. Feature Alignment** | Only projector W | 595K image-text pairs (filtered CC3M) | Learn a compatible visual tokenizer |
| **2. End-to-End Fine-Tuning** | W + LLM (Vicuna) | 158K visual instructions or ScienceQA | Learn assistant behavior |

**Training recipe (modest by modern standards):**

| Stage | Hardware | Time | Epochs | LR | Batch | Trainable Params |
|-------|----------|------|--------|-----|-------|------------------|
| Alignment | 8× A100 | 4h | 1 | 2e-3 | 128 | W only |
| LLaVA chat | 8× A100 | 10h | 3 | 2e-5 | 32 | W + Vicuna |

Implementation details: Adam, no weight decay, cosine schedule, 3% warmup, FSDP, gradient checkpointing, BF16, TF32.

> **Key Point:** Separating alignment from behavior learning keeps the architecture simple and makes the data contribution legible.

### 10.2.5 Evaluation: GPT-4 as a Judge

LLaVA changes the evaluation question from "what is in the image?" to "did the assistant answer the request well?"

**LLaVA-Bench splits:**

| Split | Content | Purpose |
|-------|---------|---------|
| **COCO** | 30 COCO images, 90 questions | Clean ablations |
| **In-the-Wild** | 24 diverse images, 60 questions | Real generalization stress tests |

**Scoring protocol:**
```
Image + question → LLaVA answer
                        ↓
              Reference answer (from text-only GPT-4)
                        ↓
                    GPT-4 judge
                        ↓
                   1–10 score
```

Score dimensions: helpfulness, relevance, accuracy, detail.

**Results (In-the-Wild):**

| Model | Score |
|-------|-------|
| OpenFlamingo | 19.1 |
| BLIP-2 | 38.1 |
| **LLaVA** | **67.3** |

> **Key Result:** The gap is largest on complex reasoning (81.7 vs 32.9 for BLIP-2), showing that assistant alignment matters more than encoder size.

### 10.2.6 Legacy and Follow-ups

| Date | Model | Improvement |
|------|-------|-------------|
| Apr 2023 | Original LLaVA | Synthetic instruction data, simple connectors |
| Oct 2023 | LLaVA-1.5 | Higher resolution, stronger vision backbone |
| Jan 2024 | LLaVA-NeXT | Better reasoning, broader modalities |
| Aug 2024 | LLaVA-OneVision | Unified image + video understanding |

What persisted: synthetic instruction data, simple connectors, staged training, open release culture.

## 10.3 Beyond LLaVA: StableLLaVA and ChartLlama

### 10.3.1 StableLLaVA

StableLLaVA enhances visual instruction tuning with **synthesized image-dialogue data**. It addresses data scarcity by generating higher-quality synthetic conversations with stronger visual grounding.

### 10.3.2 ChartLlama

ChartLlama is a multimodal LLM specialized for **chart understanding and generation**:
- Reads bar charts, line charts, pie charts, and tables
- Generates charts from natural language descriptions
- Performs numerical reasoning over visual data

## 10.4 Latent Diffusion and Stable Diffusion

> For the mathematical foundations of DDPM and LDM, see **Chapter 9**.

### 10.4.1 System-Level Context

Stable Diffusion v1 is a latent diffusion model conditioned on CLIP text embeddings. It was trained on:
- **LAION-2B-en**: 2 billion English image-text pairs
- **LAION-Aesthetics v2**: Fine-tuning subset filtered for aesthetic quality (score ≥ 5)

This operationalizes the LDM recipe into the text-to-image system that became culturally visible.

### 10.4.2 Cross-Attention in Detail

Inside the U-Net denoiser, cross-attention layers inject text conditioning:

- **Q:** from UNet spatial features
- **K, V:** from text encoder $\tau_\theta(y)$

```
Image features (UNet) ──Q──┐
                            ├──→ Cross-Attention ──→ Conditioned features
Text embeddings ──────K,V─┘
```

The original LDM paper used a BERT tokenizer and transformer conditioner. Stable Diffusion v1 switched to a **frozen CLIP ViT-L/14 text encoder**, but the cross-attention mechanism remained the same.

## 10.5 Controllable Generation

| Method | Mechanism | Use Case |
|--------|-----------|----------|
| **ControlNet** | Duplicate U-Net encoder layers, add zero-convolution adapters | Control composition with edge/pose/depth maps without retraining base model |
| **IP-Adapter** | Decoupled cross-attention path for image prompts | Transfer style/content from reference images |

> **Key Concept:** ControlNet and IP-Adapter add controllability **without modifying the base diffusion model**, making them lightweight and composable. Users can stack multiple ControlNets (e.g., pose + depth) for fine-grained control.

## 10.6 Practice: ComfyUI Workflows

ComfyUI represents image generation as a **node graph**. Each node performs one operation, and edges define data flow.

### 10.6.1 The Six Core Nodes

| # | Node | Function |
|---|------|----------|
| 1 | **Load Checkpoint** | Loads model (UNet + CLIP + VAE) |
| 2 | **CLIP Text Encode** | Converts prompts into conditioning vectors |
| 3 | **Empty Latent** | Sets canvas size |
| 4 | **KSampler** | Runs the denoising loop |
| 5 | **VAE Decode** | Converts latent back to pixels |
| 6 | **Save Image** | Writes PNG file |

### 10.6.2 KSampler Parameters

| Parameter | Meaning | Typical Value |
|-----------|---------|---------------|
| **seed** | Reproducibility | fixed or random |
| **steps** | Denoising iterations | 20–50 |
| **cfg** | Prompt strength | 7–8 |
| **sampler** | Trajectory algorithm | euler_a, dpmpp_2m |
| **denoise** | Amount of change | 1.0 (full generation) |

> **Key Concept:** Once these six nodes make sense, larger workflows (inpainting, img2img, ControlNet) are just additional nodes plugged into the same graph. The workflow file itself becomes a **reproducible recipe**.

## 10.7 Takeaways

1. **Data format changes behavior.** LLaVA's key insight was reformatting existing captions into instruction-following dialogues.
2. **Alignment before instruction tuning is not optional.** Stage 1 (projector training) protects the LLM's pretrained knowledge.
3. **Simple interfaces can be enough when the data is right.** A single linear projection matrix was sufficient.
4. **Controllability comes from conditioning paths, not base model retraining.** ControlNet and IP-Adapter prove this.

---

# 11 Personalized Generation and Agentic AI

> **Source:** SCI 1003 Class 11, Dr. Chi Zhang @ Westlake AGI Lab  
> Part A covers how text-to-image systems learn new subjects, styles, or identities. Part B covers how language models become systems that act.

---

## Part A: Personalized Image Generation

## 11.1 Motivation: Why Prompt Engineering Is Not Enough

A pretrained model knows "dog," but not **your dog**. Generic prompts describe categories; they cannot upload a new identity by words alone.

| Level | Example | Model Knowledge |
|-------|---------|-----------------|
| **Category** | "a dog" | Pretraining already knows it |
| **Instance** | "my dog" | The model has never seen it |

**Personalization** adds concept memory, then prompts can reuse it. The payoff is **compositional reuse**: one learned concept can enter new scenes, styles, and contexts.

### 11.1.1 The Personalization Triangle

Three competing goals:

| Goal | Meaning | Tension |
|------|---------|---------|
| **Identity fidelity** | Looks like the target | Pushes toward overfitting |
| **Editability** | Obeys new prompts | Pushes toward generality |
| **Efficiency** | Few images, little compute | Constrains model capacity |

> **Key Point:** Push one corner too hard and another usually pays. Every method makes a different trade-off.

### 11.1.2 Method Taxonomy

| Route | Mechanism | Strength | Weakness |
|-------|-----------|----------|----------|
| **Prompt-only** | No new weights | Zero cost | Weak for unseen concepts |
| **Embedding tuning** | New token embedding | Tiny artifact | Limited capacity |
| **Model adaptation** | Fine-tune or adapters | Best fidelity | Higher compute |
| **Reference-conditioned** | Image encoder + control path | No training | Requires reference at inference |

## 11.2 Textual Inversion

Textual Inversion learns a **pseudo-word** for a concept.

**Setup:**
- Input: a few concept images
- Output: one learned embedding $v^*$
- Use the pseudo-word $S^*$ inside normal prompts

### 11.2.1 Method

```
Prompt: "A photo of S*"
          │
          ▼
    Tokenizer routes S* → v*
          │
          ▼
    LDM (frozen) generates image
```

Only $v^*$ changes. The generator and text encoder stay frozen.

**Objective:**

$$v^* = \arg\min_v \mathbb{E}\left[ \| \epsilon - \epsilon_\theta(z_t, t, c_\theta(y_v)) \|^2 \right]$$

Same denoising target as diffusion training, but only the pseudo-word embedding is trainable.

### 11.2.2 Trade-offs

| Advantages | Limitations |
|------------|-------------|
| Tiny artifact to store | One embedding has limited capacity |
| Base model stays frozen | Hard subjects lose identity |
| Pseudo-word composes with prompts | Editability and fidelity still trade off |

> **Best Practice:** Use Textual Inversion for small concept shifts and lightweight teaching examples. It is elegant because it is small, and limited because it is small.

## 11.3 DreamBooth

DreamBooth turns a **rare token** into an instance handle.

**Pattern:** "a [V] dog wearing sunglasses"

### 11.3.1 Training

| Step | Action |
|------|--------|
| **Input** | 3–5 subject images |
| **Binding** | Rare token + class word (keeps semantic grounding) |
| **Training** | Fine-tune the generator to make [V] refer to the subject |
| **Output** | Re-contextualized samples in new scenes |

### 11.3.2 Prior Preservation Loss

DreamBooth motivates the **fidelity-editability trade-off** explicitly through its loss design:

$$\mathcal{L} = \underbrace{\mathbb{E}\left[ \| \epsilon - \epsilon_\theta(x_{\text{instance}}) \|^2 \right]}_{\text{Instance loss}} + \lambda \underbrace{\mathbb{E}\left[ \| \epsilon - \epsilon_\theta(x_{\text{prior}}) \|^2 \right]}_{\text{Prior loss}}$$

- **Instance loss:** Make $[V]$ dog reproduce the target dog
- **Prior loss:** Keep "dog" broad enough to remain a class

> **Key Concept:** Without prior preservation, the model overfits to the instance and forgets the class. With too little adaptation, identity is weak. Prior preservation loss explicitly balances this.

## 11.4 LoRA: Low-Rank Adaptation

LoRA asks: **do we really need to move every weight?**

### 11.4.1 Full Fine-Tuning vs LoRA

| Aspect | Full Fine-Tuning | LoRA |
|--------|-----------------|------|
| Parameters | Update many | Update small A/B matrices |
| Memory | High | Low |
| Sharing | Harder | Easy (swap adapters) |
| Modularity | One model per subject | Mix subject/style/task adapters |

### 11.4.2 Formula

$$W' = W + \Delta W, \quad \text{where } \Delta W = B \cdot A$$

- $W$ stays **frozen**
- $A$ and $B$ are small trainable matrices
- Rank $r$ controls adapter capacity

In diffusion personalization, LoRA typically trains attention blocks while the base checkpoint remains intact.

> **Key Concept:** Personalization becomes modular when the delta is small. Artists can collect and mix LoRA files for different subjects and styles.

## 11.5 Reference-Conditioned Methods

Newer systems personalize **without any training** by using reference images at inference time:

| Method | Mechanism | Use Case |
|--------|-----------|----------|
| **IP-Adapter** | Generic image prompt adapter via decoupled cross-attention | Strong reference route |
| **PhotoMaker** | Stacked identity inputs | Personalized photos |
| **InstantID** | Identity-preserving generation | Face identity transfer |

> **Key Point:** Reference-conditioned methods shift the paradigm from "adapt after pretraining" to "train reference inputs end-to-end." The trade-off becomes concept memory vs in-context control.

## 11.6 Qwen-Image

Qwen-Image represents the **frontier** of open image generation foundation models.

### 11.6.1 Architecture

```
Text / Multimodal Instruction
        │
        ▼
Qwen2.5-VL (MLLM condition encoder)
        │
        ▼
VAE (latent space)
        │
        ▼
MMDiT (double-stream multimodal diffusion transformer)
        │
        ▼
Generated image
```

- **MSRoPE:** Multimodal Rotary Position Embedding designed for joint text-image positional encoding
- **Double-stream:** Text and image features processed in parallel under shared conditioning

### 11.6.2 Family Members

| Model | Capability |
|-------|------------|
| **Qwen-Image** | Open T2I + strong editing backbone |
| **Qwen-Image-Edit** | Reference image + instruction; preserve while changing |
| **Qwen-Image-Edit-2509** | Single + multiple image editing |
| **Qwen-Image-Edit-2511** | Stronger identity and group consistency |
| **Qwen-Image 2.0** (2026) | Unified generation + editing direction |

> **Key Concept:** The frontier is moving from durable adapters (LoRA, DreamBooth) toward **in-context control** where the model natively consumes reference images during inference.

## 11.7 Choosing a Personalization Route

| Constraint | Recommended Method |
|------------|-------------------|
| Few images, zero training | IP-Adapter / InstantID |
| Tiny artifact to share | Textual Inversion / LoRA |
| Best instance binding | DreamBooth-style fine-tuning |
| In-context editing | Qwen-Image-Edit |

---

## Part B: Agentic AI

## 11.8 From Language Models to Agents

### 11.8.1 The Capability Stack

```
Layer 1: Language Model     → Predicts text from context
Layer 2: Chatbot            → Turns prediction into dialogue
Layer 3: Agent              → Pursues goals with tools
Layer 4: Multi-Agent        → Divides work across roles
Layer 5: AI Organization    → Adds policies, evaluation, oversight
```

> **Key Concept:** The story is a shift from conversation to delegation. Each step adds one missing capability: memory, tools, planning, roles, and governance.

### 11.8.2 Why Fluency Is Not Enough

| What LLMs Are Good At | What Breaks Without a System |
|-----------------------|------------------------------|
| Summarizing messy text | Confident hallucinations |
| Drafting and translating | Stale or missing external knowledge |
| Writing code patterns | No native ability to click, buy, call |
| Connecting ideas | Long-horizon drift over many steps |
| Explaining concepts | Weak self-review when stakes are high |

> **Key Point:** A fluent model is not the same thing as a reliable worker. Agents need external feedback, constraints, and verifiable action.

## 11.9 Agent Anatomy

An agent is the **control loop around an LLM**:

```
        ┌─────────────────────────────┐
        │          LLM                │
        │    (reasoning engine)       │
        └─────────────┬───────────────┘
                      │
    ┌─────────┬───────┼───────┬─────────┐
    ▼         ▼       ▼       ▼         ▼
 Observe    Plan     Act     Check    Memory
 (read)   (decide) (tools) (verify) (store)
```

| Component | Role |
|-----------|------|
| **LLM** | Language prediction and reasoning |
| **Instructions** | Role, policy, task boundary |
| **Planner** | Next actions and stop conditions |
| **Tools** | APIs, browser, code, files, UI |
| **Memory** | Short-term and long-term state |
| **Evaluator** | Checks quality and safety |
| **Permissions** | What actions need approval |

## 11.10 ReAct: Interleaving Reasoning and Acting

The ReAct pattern alternates between thinking, tool use, observation, and revised thinking:

| Step | Example |
|------|---------|
| **Thought** | "I need the city and forecast source." |
| **Action** | Call weather API or browser search. |
| **Observation** | Forecast: rain, 18-22°C, windy. |
| **Thought** | "Now convert weather into useful advice." |
| **Action** | Draft concise message for the user. |

> **Key Concept:** The tool result changes the next reasoning step. This makes the system more grounded and inspectable than one long hidden answer.

## 11.11 Tool Use at the Prompt Level

### 11.11.1 Before the Tool

The first LLM call contains the task plus a menu of possible tools. The model decides whether a tool is needed before answering.

```
SYSTEM: You are a helpful travel assistant. 
        If weather matters, use Weather Lookup before giving advice.

USER: "I'm leaving for Paris tomorrow morning. 
      Should I bring an umbrella?"

LLM: Tool request: Weather Lookup(city=Paris, time=tomorrow morning)
```

This is already an agent step: the assistant message is an **action request**, not the final answer.

### 11.11.2 After the Tool

The tool result is inserted into the next prompt as an observation:

```
CONTEXT NOW:
1. System prompt
2. User question
3. Assistant's weather tool request
4. New observation: "Paris: light rain, 17°C, wind 18 kph"

LLM FINAL REPLY: "Yes, bring a compact umbrella. 
                   Wear a light jacket..."
```

> **Key Point:** The model did not become smarter between turns. **The prompt changed**: it now contains the weather observation. An agent loop is a repeated prompt: ask model → receive action → add observation → ask model again.

## 11.12 GUI Agents

GUI agents move action into the interface itself:

| Aspect | Approach |
|--------|----------|
| **Perception** | Screen pixels |
| **Execution** | Structured actions (tap, type, swipe) |
| **Generalization** | Spans apps and tasks |

Example: AppAgent uses screen observations and simplified actions (tap, swipe, text input, back) without relying on privileged backend APIs.

## 11.13 Multi-Agent Systems

### 11.13.1 Role Decomposition

Multi-agent systems split roles, not just prompts:

| Role | Function |
|------|----------|
| **Planner** | Decompose task; decide who does what |
| **Executor** | Act with tools and edits |
| **Critic** | Verify; catch gaps and regressions |
| **Shared State** | Coordinate memory, messages, artifacts |

### 11.13.2 MetaGPT

MetaGPT makes a software team out of agent roles:
- Encode SOP-like workflows
- Assign specialist roles (product manager, architect, engineer, tester)
- Pass structured artifacts between agents

> **Key Concept:** Multi-agent value comes from **useful handoffs**, not from having many agents. Each role should produce an artifact that the next role can consume.

## 11.14 Summary: Think in Layers

| Layer | Job | Key Insight |
|-------|-----|-------------|
| **LLM** | Language prediction and reasoning from context | Do not confuse fluency with reliability |
| **Agent** | Goal loop with tools, memory, and feedback | Agents need feedback, tools, and constraints |
| **Multi-Agent** | Roles, protocols, shared state, oversight | Value comes from useful handoffs |

> **Best Practice:** Read an agent as a **message transcript**, not as code. The important object is the sequence of visible messages: user prompt, assistant tool request, tool observation, final answer.

## 11.15 Practice: Building a Simple Agent

The course provides a restaurant reservation agent using the OpenAI API:

```python
from openai import OpenAI
import json
import datetime

class CustomerServiceAgent:
    def __init__(self, base_url, api_key, model="qwen-plus", max_retries=3):
        self.client = OpenAI(base_url=base_url, api_key=api_key)
        self.model = model
        self.max_retries = max_retries
        self.conversation_history = []
        
        # System prompt defines the agent's role and constraints
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        self.system_prompt = f"""You are a restaurant reservation assistant.
Today's date is {current_date}.
1. Extract reservation time and number of people from user input
2. Format as JSON: {{"time": "YYYY-MM-DD HH:MM", "people": "X"}}
3. If information is missing, actively ask the user
4. Only return JSON when complete, otherwise continue dialogue"""
        
        self.conversation_history.append(
            {"role": "system", "content": self.system_prompt}
        )
    
    def process_query(self, user_input):
        self.conversation_history.append(
            {"role": "user", "content": user_input}
        )
        
        for attempt in range(self.max_retries):
            try:
                response = self.client.chat.completions.create(
                    messages=self.conversation_history,
                    model=self.model,
                )
                assistant_response = response.choices[0].message.content
                self.conversation_history.append(
                    {"role": "assistant", "content": assistant_response}
                )
                self.try_extract_reservation(assistant_response)
                return assistant_response
            except Exception as e:
                if attempt < self.max_retries - 1:
                    time.sleep((attempt + 1) * 2)
                    continue
                return f"Error: {str(e)}"
    
    def try_extract_reservation(self, response_text):
        try:
            start_idx = response_text.find("{")
            end_idx = response_text.rfind("}")
            if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
                json_str = response_text[start_idx:end_idx + 1]
                reservation_data = json.loads(json_str)
                if "time" in reservation_data and "people" in reservation_data:
                    self.save_reservation(reservation_data)
                    return True
            return False
        except:
            return False
    
    def save_reservation(self, reservation_data):
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("reservations.txt", "a", encoding="utf-8") as f:
            f.write(f"[{current_time}] Time: {reservation_data['time']}, "
                    f"People: {reservation_data['people']}\n")
```

> **Key Concept:** This minimal agent demonstrates the core loop: system prompt defines behavior, user input triggers reasoning, the model may output structured data (JSON), and the wrapper handles persistence. No special "agent framework" is required — just careful prompt engineering and state management.

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



---

# 12 Classic Agent Works

> **Source:** SCI 1003 Class 12, Dr. Chi Zhang @ Westlake AGI Lab  
> This chapter provides deep dives into landmark agent systems—AutoGPT, Generative Agents, MetaGPT, and AppAgent—and outlines the course team project requirements. Each case study illustrates a different facet of agent design: open-ended goal pursuit, social simulation, structured multi-role collaboration, and GUI-level interaction.

---

## Part A: Landmark Agent Systems

## 12.1 AutoGPT

### 12.1.1 Background: From Answering to Doing

AutoGPT represents the shift from **question-answering** to **goal-driven execution**. Users no longer specify every step; they provide an end goal. The agent must decide what to search, write, and do next. This exposes new problems: plan drift, tool failure, and runaway cost.

### 12.1.2 Core Idea: The User Gives Only the Goal

A typical AutoGPT setup looks like this:

```
Name: ResearchGPT
Role: autonomous research assistant
Goals:
  1. research AI agent applications in education in 2026
  2. identify 5 representative projects
  3. produce a lecture-handout outline
Constraints:
  - cite sources
  - save notes to workspace
  - stop when enough evidence is collected
```

**Three-step decomposition:**

| Step | Action |
|------|--------|
| **1. Decompose** | Break the goal into search, filtering, synthesis, and writing |
| **2. Use tools** | Browse pages, read files, draft text, and update memory |
| **3. Self-check** | Decide whether the current evidence is enough or more is needed |

> **Key Point:** The prompt is not the answer; it defines an **executable target state**.

### 12.1.3 Method: The Minimal Control Loop

AutoGPT's core is a closed loop of prompt, tools, and state:

```
1. Thought
   The LLM states its current understanding, subgoal, and rationale.

2. Command
   It selects one available action: search, read file, write file, etc.

3. Observation
   The system returns tool results to the LLM as the next observation.

4. Memory
   Important facts are written into workspace or memory to avoid repeated search.
```

> **Key Concept:** The core is not one prompt; it is the **closed loop** of prompt, tools, and state.

### 12.1.4 Tool Layer

| Tool | Function |
|------|----------|
| **Browser / Search** | Search information, open web pages, extract text for research |
| **File System** | Create working folders, write notes, persist intermediate results |
| **Code / Shell** | Run scripts and process data (introduces security risks) |
| **Plugin / API** | Connect email, calendars, databases, business systems |

> **Key Point:** A larger action space means more capability, and also more need for boundaries and audit.

### 12.1.5 Memory Design

| Type | Function |
|------|----------|
| **Working memory** | Short-term context stores recent observations and decisions |
| **Long-term memory** | Stores goals, facts, file paths, intermediate conclusions |

> **Trade-off:** Good memory reduces repeated search, but it can also preserve mistakes.

### 12.1.6 Failure Mode: Goal Drift and Over-Looping

**Example failure trace:**

```
User goal: write a competitor analysis
Round 1: search competitors
Round 2: search more competitors
Round 3: search market reports
Round 4: search news
Round 5: search again...
```

| Aspect | Detail |
|--------|--------|
| **Symptom** | Keeps searching and never moves into writing or convergence |
| **Cause** | Goal is too broad, evaluator is weak, tool results are noisy |
| **Fix** | Decompose the task, set a budget, require checkable artifacts each round |

### 12.1.7 Best Practice: Goals as Artifacts

Turn a broad goal into **checkable artifacts**:

```
Task: prepare materials for Lecture 1 on agents
Deliverables:
  1. source_list.md
  2. 5-slide outline.md
  3. open_questions.md

Budget:
  - max 6 tool calls
  - every call must update one deliverable
  - stop after all files exist
```

> **Key Concept:** Completion is defined by whether the files exist and contain enough content. Writing goals as artifacts is usually more reliable than writing them as wishes.

### 12.1.8 AutoGPT Takeaways

| Aspect | Insight |
|--------|---------|
| **Strengths** | General goals, open tools, fast prototyping, powerful product imagination |
| **Weaknesses** | Weak evaluation, loops, hallucination, goal drift, budget burn |
| **Method lesson** | Turn prompts into control protocols and tool calls into auditable actions |
| **Influence** | Many later frameworks add roles, documents, environment constraints, and evaluation on top |

> **One-line memory:** AutoGPT made "LLMs can act on their own" into a runnable engineering idea.

## 12.2 Generative Agents (Smallville)

### 12.2.1 Background: From Scripted NPCs to Generated Social Behavior

Traditional game NPCs rely on hand-written scripts with limited coverage. LLMs can generate open language, but need long-term state to stay consistent. Generative Agents aim to let a group of agents interact naturally in one environment.

### 12.2.2 Task Setup: Continuous Daily Life

Each character has a home, job, relationships, and current plan. The environment provides observable events (who is where, what was said). The output is the next natural-language behavior, then mapped into town actions.

### 12.2.3 Memory Stream

Every observation is written into a **stream of events**. Retrieval combines:

| Factor | Role |
|--------|------|
| **Recency** | Recent events are more accessible |
| **Importance** | Significant events are prioritized |
| **Relevance** | Events related to current context are retrieved |

> **Key Concept:** The agent does not need to stuff all history into the prompt. The memory stream supplies retrieved facts on demand.

### 12.2.4 Reflection: Compressing Memories into Beliefs

```
1. Observe    → Record environmental events and conversations
2. Score      → Assign importance to memories
3. Ask        → Generate higher-level questions ("what is my relationship with this person?")
4. Summarize  → Synthesize related memories into a new reflection memory
```

> **Key Point:** Reflection helps agents form reusable explanations, not just remember facts.

### 12.2.5 Planning: From Daily Schedule to Immediate Action

| Level | Function |
|-------|----------|
| **Daily plan** | Coarse schedule: breakfast, work, rest |
| **Hourly plan** | Break schedule into hourly segments |
| **Reactive update** | Locally revise plan when new events occur |
| **Action output** | Output next concrete behavior or dialogue |

> **Key Concept:** Planning is not a rigid script; it gives stability while allowing interruptions.

### 12.2.6 Dialogue Generation

The system first retrieves memories related to the people, place, and event. The prompt includes:
- Persona
- Current environment
- Retrieved memories

The LLM replies in a way that fits the character's relationships and history.

### 12.2.7 Experimental Result

| Architecture | Behavior Believability |
|-------------|------------------------|
| **Full architecture** | Highest |
| No reflection | Lower |
| No planning | Lower |
| No memory | Worst |

> **Conclusion:** Believable behavior is not just the LLM; memory, reflection, and planning support it together.

## 12.3 MetaGPT

### 12.3.1 Background: From One Agent to a Software Company

Complex software cannot be completed reliably from one prompt. Real teams rely on roles, reviews, and documents to pass information. MetaGPT imports these engineering workflows into a multi-agent framework.

> **Key Question:** Why can't multiple LLM agents simply free-chat in a group chat?

### 12.3.2 SOP: Turning Collaboration from Chat into Process

**Standard Operating Procedures (SOPs)** constrain collaboration:

- Each role knows what to read and what to produce
- Intermediate artifacts connect the workflow instead of free-form chat memory
- SOPs reduce role confusion and duplicated work

### 12.3.3 Role Design

| Role | Responsibility |
|------|----------------|
| **Product Manager** | Clarify requirements; produce PRDs, user stories, constraints |
| **Architect** | Decompose modules, design interfaces, set technical structure |
| **Engineer** | Implement code according to design; handle dependencies and files |
| **QA / Reviewer** | Generate tests, inspect defects, feed back revisions |

> **Key Concept:** The value of roles is **constrained perspective**: each role owns its artifact.

### 12.3.4 Intermediate Documents as Interface

PRDs, system designs, task lists, and code files are **checkable artifacts**. Later roles read earlier artifacts instead of guessing requirements again. Documents make multi-round, multi-role collaboration traceable.

### 12.3.5 Message Pool Architecture

| Feature | Function |
|---------|----------|
| **Structured messages** | Carry sender, receiver, content type, artifact path |
| **Selective subscription** | Roles only attend to messages relevant to their responsibility |
| **Action trigger** | After receiving prerequisite artifacts, a role runs its Action |
| **Persist artifacts** | Results are written as files or documents for later roles |

> **Key Point:** The key to multi-agent systems is not more talking, but **routing and artifact contracts**.

### 12.3.6 Experimental Result

| Approach | Code Task Performance |
|----------|----------------------|
| Single model / simple baseline | Lower |
| Multi-role without strong SOP | Improved |
| **MetaGPT with SOP** | **Higher** |

> **Conclusion:** Making the process explicit matters more than merely adding agents.

### 12.3.7 MetaGPT Takeaways

| Aspect | Insight |
|--------|---------|
| **Core contribution** | Organize software development with roles, SOPs, structured messages, and document artifacts |
| **Value** | Break complex tasks into checkable and traceable intermediate results |
| **Method lesson** | Agent collaboration needs interfaces, not free-form chat |

> **One-line memory:** MetaGPT makes an agent team look like an engineering process, not a lively group chat.

## 12.4 AppAgent

### 12.4.1 Background: Agents as Smartphone Users

Many real user tasks happen inside mobile apps: maps, email, video, shopping, music, reviews. APIs may not be open, and web automation may not apply. A GUI-level agent is closer to ordinary users' operation world.

### 12.4.2 Task Setup

Input a goal (e.g., finding an email in Gmail or searching a place on Maps). Each step receives the current screenshot and interactive elements. The output is one action; after execution, the next round begins.

### 12.4.3 Input Representation: Multimodal State

| Modality | Information |
|----------|-------------|
| **Screenshot** | Visual context: icons, text, layout |
| **XML** | Interactive elements and their attributes |
| **Overlay IDs** | Numbered elements on the screenshot so the model can reference them |

### 12.4.4 Action Space

AppAgent uses deliberately human-like basic gestures:

| Action | Description |
|--------|-------------|
| **Tap(element)** | Tap a numbered element to open, select, or confirm |
| **Long_press(element)** | Long-press to trigger menus or special selection |
| **Swipe(element, direction, dist)** | Swipe to browse lists or switch pages |
| **Text / Back / Exit** | Input text, go back, or end the task |

> **Key Point:** A small action space reduces parsing difficulty and makes experiments more controllable.

### 12.4.5 Two-Phase Learning

| Phase | What Happens |
|-------|-------------|
| **Exploration** | Agent autonomously taps and swipes, observing before/after screens. Records each element's function into an app-specific document |
| **Demonstration** | Human demonstrates task completion; system records UI element functions (not fixed trajectories) |

> **Key Concept:** The document records **UI element functions**, not a fixed trajectory. This improves generalization to similar tasks or UI changes.

### 12.4.6 Deployment Prompt Structure

Each prompt includes:
- Current screen (screenshot + interactive elements)
- Generated app document
- Action schema

The model outputs: **Observation → Thought → Action → Summary**. Summary acts as short-term memory; Exit marks completion.

### 12.4.7 Experimental Results

Success rates over 45 tasks:

| Method | Success Rate |
|--------|-------------|
| GPT-4 baseline | 2.2% |
| AppAgent (no doc) | 48.9% |
| Auto exploration | 73.3% |
| Watching demos | 84.4% |
| **Manual doc** | **95.6%** |

> **Conclusion:** Long-term GUI knowledge is extremely valuable, especially app-specific documents. As task steps increase, the gap widens—document-assisted methods maintain higher success in long action chains.

---

## Part B: Course Team Project Briefing

## 12.5 Project Overview

### 12.5.1 Objective

Design and implement an **original AI application** that leverages techniques introduced in this course, including foundation models, generative AI, or agent-based systems.

### 12.5.2 Core Requirements

| # | Requirement | Detail |
|---|-------------|--------|
| **1** | **Innovation First** | Focus on a novel use case—not a reproduction of commonly seen demos or existing products |
| **2** | **Technology Integration** | Go beyond calling a single API or model. Combine multiple AI components (LLM reasoning, generation, perception) |
| **3** | **Team Collaboration** | Reflect a reasonable workload for a 4-person team with clear division of tasks |

### 12.5.3 Proposal Examples

**Example 1: Multi-Agent System for Real-World Problem Solving**
- Emphasizes decentralized intelligence and task decomposition
- Distinct agent roles + coordination + a novel scenario
- Can integrate LLM-based planning, agent communication protocols, tool-using agents

**Example 2: Creative Generative AI Workflow**
- Design a generative AI pipeline using ComfyUI or WebUI
- Combine multiple generative models into a customized, multi-step workflow
- Scenarios: personalized image generation/editing, video synthesis, LLM-enabled semantic control

## 12.6 Grading Policy

### 12.6.1 Team-Level Evaluation (100%)

| Component | Weight | Criteria |
|-----------|--------|----------|
| **Technical Report** | 30% | Clarity, structure, depth of analysis, quality of writing |
| **Presentation** | 30% | Effectiveness of communication, visual aids, delivery, Q&A ability |
| **Technical Quality** | 40% | Problem difficulty (10%), creativity of approach (10%), completeness (10%), amount of work (10%) |

### 12.6.2 Individual Contribution Evaluation

Each student submits a confidential peer evaluation:

| Rating | Adjustment | Condition |
|--------|-----------|-----------|
| **Significantly above average** | +5% bonus | At least two teammates independently select this option |
| **Roughly average** | 0% (full team score) | Default if consensus is not reached |
| **Significantly below average** | -10% penalty | At least two teammates independently select this option |

## 12.7 Presentation Guidelines

- **Duration:** 10-minute slides presentation in English + 5-minute Q&A
- **Advised sections:**
  1. **Motivation** — reason for choosing the topic and its importance
  2. **Methodology** — approach and techniques used
  3. **Demonstration** — live demo, video, or suitable format showcasing functionality
  4. **Experimental Results** — results on real-world or simulated datasets
  5. **Summary and Conclusion** — achievements, lessons learned, future improvements

## 12.8 Technical Report Guidelines

### 12.8.1 Overall Structure

```
01 Introduction      → Context, motivation, proposed solution, contributions
02 Related Work     → Relevant AI technologies, related applications, comparison/positioning
03 Method           → System overview, key components, algorithms, implementation details
04 Experiments      → Setup, qualitative results, quantitative evaluation, ablation study
05 Conclusion       → Summary and future directions
```

### 12.8.2 Introduction Structure

1. **Background** — broader area, enough context for unfamiliar readers
2. **Motivation & Problem Statement** — why interesting/challenging, what is missing
3. **Proposed Solution (Overview)** — high-level summary, key AI techniques used
4. **Contributions / Achievements** — 2–3 bullet points of main contributions

### 12.8.3 Method Section Best Practices

- Start with a high-level system diagram
- Break down into major components/modules
- Include mathematical formulations if applicable
- Add pseudocode or flowchart for agent systems
- Mention tools, models, APIs, platforms used

### 12.8.4 Experiment Section Best Practices

| Aspect | What to Include |
|--------|----------------|
| **Setup** | Task/scenario, datasets, prompts, test inputs, runtime environment |
| **Qualitative Results** | Example outputs with explanation of what they demonstrate |
| **Quantitative Evaluation** | Numerical metrics in tables or charts |
| **Ablation Study** | Compare with/without key components to demonstrate necessity |

> **Key Point:** Evidence should show that the method works **and** why the design choices matter.

## 12.9 Tutorial: Multi-Agent Discussion

### 12.9.1 Purpose

Showcase collaboration among purpose-driven LLM agents with distinct personalities.

### 12.9.2 Key Concepts

| Concept | Description |
|---------|-------------|
| **Agent personalities** | Each agent adopts a specific alignment/perspective (e.g., Lawful Good, Chaotic Neutral, Lawful Evil) |
| **Turn-based discussion** | Each turn selects a speaker, invokes an LLM, records the response for the next step |
| **StateGraph orchestration** | Graph-based state machine manages conversation flow |

### 12.9.3 Setup

- **Defined rounds:** Structured turns with speaker selection
- **Expected outcome:** Diverse perspectives converging on a team activity plan

> **Key Concept:** Three purpose-driven agents discuss the same task from different perspectives, demonstrating how role-defined agents produce richer, more balanced decisions than a single model.

---

> **Best Practice (Agent Systems):** Read an agent as a **message transcript**, not as code. The important object is the sequence of visible messages: user prompt, assistant tool request, tool observation, final answer. This applies to AutoGPT's loop, MetaGPT's document handoffs, and AppAgent's screen-action pairs alike.
