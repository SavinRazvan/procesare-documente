# GeoJSON Processor V2

> Professional document processing system for GeoJSON files with comprehensive data validation, duplicate detection, and centralized output generation.

## 🚀 Quick Start

```bash
# Setup environment
conda create -n .proc_doc python=3.11 -y
conda activate .proc_doc

# Navigate to project
cd /home/razvansavin/Projects/procesare-documente

# Process all models
python3 _process_all.py _input _output
```

## 📋 Features

- **23 Individual Processors**: Handle specific model types
- **Master Processor**: Orchestrates all individual processors
- **Configuration-Driven**: JSON-based model definitions
- **Professional Logging**: Comprehensive error handling
- **No External Dependencies**: Python standard library only
- **Centralized Output**: Unified processing results

## 📁 Project Structure

```
procesare-documente/
├── _input/                    # Input GeoJSON files
├── _output/                   # Processed output files
├── config/                    # Configuration files
├── src/                       # Core processing engine
├── _process_all.py            # Master processor
├── _[model].py               # Individual processors (23 files)
└── README.md                  # This file
```

> **For detailed architecture overview, see [TUTORIAL.md](TUTORIAL.md)**

## 📚 Documentation

- **[TUTORIAL.md](TUTORIAL.md)** - Complete user guide with setup instructions
- **[doc_input_headers.md](doc_input_headers.md)** - Field specifications and technical reference
- **[requirements.txt](requirements.txt)** - Dependencies information

## 🔧 Requirements

- **Python**: 3.11+
- **Conda**: For environment management
- **No External Dependencies**: Uses only Python standard library

## 📊 Supported Models

### Main Layers (14)
- `camereta`, `enclosure`, `hub`, `localitati`, `stalpi`
- `zona_hub`, `zone_interventie`, `case`, `spliter`
- `zona_pon`, `zona_spliter`, `fibra`, `scari`
- `zona_pon_re_ftth1000`

### Search Layers (4)
- `fttb_search`, `scari_search`, `camereta_search`, `enclosure_search`

## 🎯 Usage Examples

```bash
# Process specific models
python3 _process_all.py _input _output --models camereta case

# Process without duplicate detection
python3 _process_all.py _input _output --no-duplicates

# Individual processor
python3 _camereta.py _input _output
```

## 📈 Performance

- **Lightweight**: No external dependencies
- **Fast**: Optimized for large datasets
- **Memory Efficient**: Streaming processing
- **Scalable**: Handles thousands of features

## 🛠️ Development

```bash
# Test individual processor
python3 _camereta.py _input _output

# Test master processor
python3 _process_all.py _input _output --models camereta

# Check help
python3 _process_all.py --help
```

## 📞 Support

For issues or questions:
1. Check [TUTORIAL.md](TUTORIAL.md) for usage instructions and setup
2. Review [doc_input_headers.md](doc_input_headers.md) for field specifications
3. Check console output for error messages
4. Verify input file formats and naming

---

**Author**: Savin Ionut Razvan  
**Version**: 2025.10.05  
