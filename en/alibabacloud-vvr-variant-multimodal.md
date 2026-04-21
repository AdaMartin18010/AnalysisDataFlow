# Alibaba Cloud VVR 11.6.0: Variant Type and Multimodal AI

> **Stage**: Flink/ecosystem | **Prerequisites**: [Flink SQL Guide](flink-table-sql-complete-guide.md) | **Formalization Level**: L3-L4
> **Translation Date**: 2026-04-21

## Abstract

Alibaba Cloud VVR 11.6.0 introduces the Variant semi-structured dynamic type for efficient JSON-like data storage and query, along with built-in multimodal AI functions for Flink SQL.

---

## 1. Definitions

### Def-F-ECO-01 (Variant Data Type)

**Variant** is a semi-structured dynamic type for efficient JSON-like data:

$$\text{Variant} = \{ (k_i, v_i, \tau_i) \mid k_i \in \text{Keys}, v_i \in \text{Values}, \tau_i \in \mathcal{T} \}$$

where $\mathcal{T} = \{ \text{NULL}, \text{BOOLEAN}, \text{INT64}, \text{FLOAT64}, \text{STRING}, \text{ARRAY}, \text{OBJECT} \}$.

**Field access syntax**:

```sql
-- Dot notation (for valid identifiers)
SELECT variant_column.field_name FROM events;

-- Bracket notation (dynamic keys, special characters)
SELECT variant_column['key-with-dash'] FROM events;
SELECT variant_column['nested']['deep'] FROM events;
```

### Def-F-ECO-02 (AI Function Multimodal Capabilities)

VVR 11.6.0 AI Functions enable multimodal LLM calls directly in Flink SQL:

| Capability | Function Example | Description |
|-----------|-----------------|-------------|
| PDF to images | `AI_PDF_TO_IMAGES(pdf_url)` | Convert PDF pages to image sequence |
| Image quality | `AI_IMAGE_QUALITY(image_url)` | Detect blur, low resolution |
| OSS file extract | `AI_EXTRACT_FILE(oss_url)` | Extract OSS object content |
| Base64 pass-through | `AI_VL_PREDICT(base64_image, prompt)` | Direct Base64 image input |
| Qwen-VL call | `AI_QWEN_VL(image_urls, prompt)` | Tongyi Qianwen vision model |

---

## 2. Example

```sql
-- Extract product info from Variant column
SELECT
    product_id,
    product_info['name'] as product_name,
    product_info['price'] as price,
    product_info['tags'][0] as primary_tag
FROM product_stream;

-- Multimodal AI: analyze product images
SELECT
    product_id,
    AI_QWEN_VL(image_url, 'Describe this product') as description
FROM product_images;
```

---

## 3. References
