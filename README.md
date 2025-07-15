# Beckn Protocol Validator

A web-based validation tool for Beckn protocol JSON payloads using AI agents and MCP (Model Context Protocol) servers.

## 🎯 Overview

This application provides a Gradio-based web interface to validate Beckn protocol JSON payloads against the specification. It uses AI agents with MCP servers to perform intelligent validation and provides detailed feedback on payload compliance. The MCP server communicates with a Beckn OAS validator service that can be either an internal Kubernetes service or the global external validator.

## ✨ Features

- **Web-based UI**: Clean Gradio interface for easy payload validation
- **AI-powered validation**: Uses OpenAI agents with MCP servers for intelligent analysis
- **Real-time validation**: Instant feedback on Beckn protocol compliance
- **Multiple action support**: Validates all Beckn actions (search, select, init, confirm, etc.)
- **Kubernetes ready**: Full deployment configuration for production environments
- **Docker optimized**: Containerized with optimized 200MB image size

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────────┐
│   Gradio UI     │───▶│   AI Agent       │───▶│   MCP Server        │
│   (Port 7860)   │    │   (OpenAI)       │    │   (Validation)      │
└─────────────────┘    └──────────────────┘    └─────────────────────┘
                                                          │
                                                          ▼
                                    ┌─────────────────────────────────┐
                                    │   Beckn OAS Validator Service   │
                                    │                                 │
                                    │  ┌─────────────────────────────┐ │
                                    │  │ Internal K8s Service        │ │
                                    │  │ (oas31-validator-service)   │ │
                                    │  │ ClusterIP in same namespace │ │
                                    │  └─────────────────────────────┘ │
                                    │                                 │
                                    │  ┌─────────────────────────────┐ │
                                    │  │ External Global Service     │ │
                                    │  │ (oas-validator.becknprotocol│ │
                                    │  │ .io/retail)                 │ │
                                    │  └─────────────────────────────┘ │
                                    └─────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- Docker
- Kubernetes cluster (for production deployment)
- OpenAI API key
- Google/Gemini API key

### Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd mcp-spec-validator
   ```

2. **Install dependencies**
   ```bash
   pip install uv
   uv sync
   ```

3. **Set environment variables**
   ```bash
   export OPENAI_API_KEY="your-openai-key"
   export GEMINI_API_KEY="your-gemini-key"
   ```

4. **Run the application**
   ```bash
   uv run ui.py
   ```

5. **Access the web interface**
   - Open http://localhost:7860 in your browser

### Docker Deployment

1. **Build the image**
   ```bash
   ./build-and-push.sh
   ```

2. **Run with Docker**
   ```bash
   docker run -p 7860:7860 \
     -e OPENAI_API_KEY="your-key" \
     -e GEMINI_API_KEY="your-key" \
     asia-south1-docker.pkg.dev/gen-lang-client-0091398941/spec-validator/ai-agent:v1
   ```

## ☸️ Kubernetes Deployment

### Prerequisites

- GKE cluster with access to Google Artifact Registry
- `kubectl` configured
- `gcloud` authenticated

### Deploy to Kubernetes

1. **Create namespace**
   ```bash
   kubectl create namespace beckn-spec
   ```

2. **Create secrets**
   ```bash
   kubectl create secret generic my-api-keys \
     --from-literal=OPENAI_API_KEY="your-openai-key" \
     --from-literal=GEMINI_API_KEY="your-gemini-key" \
     -n beckn-spec
   ```

3. **Deploy the application**
   ```bash
   kubectl apply -f k8s/k8s-deployment.yaml -n beckn-spec
   ```

4. **Check deployment status**
   ```bash
   kubectl get pods -n beckn-spec
   kubectl get services -n beckn-spec
   ```

### Access the Application

- **External IP**: Get the LoadBalancer IP from `kubectl get services -n beckn-spec`
- **Internal access**: `spec-validator-service.beckn-spec.svc.cluster.local:80`

## 📁 Project Structure

```
mcp-spec-validator/
├── ui.py                 # Gradio web interface
├── my_agent.py           # AI agent implementation
├── mcp_server.py         # MCP server for validation
├── pyproject.toml        # Python dependencies
├── Dockerfile            # Container configuration
├── .dockerignore         # Docker build exclusions
├── build-and-push.sh     # Build and push script
├── k8s/
│   └── k8s-deployment.yaml  # Kubernetes deployment
└── README.md             # This file
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key for AI agent | Required |
| `GEMINI_API_KEY` | Google/Gemini API key | Required |
| `BECKN_VALIDATOR_URL` | Beckn validator service URL | `http://oas-validator.becknprotocol.io/retail` |

### Validator Service Options

The application can use either of two Beckn OAS validator services:

1. **Internal Kubernetes Service** (Recommended for production)
   - Service: `oas31-validator-service` (ClusterIP in same namespace)
   - URL: `http://oas31-validator-service`
   - **Advantages**: Faster response, no external dependencies, controlled lifecycle

2. **External Global Service** (Fallback)
   - Service: `http://oas-validator.becknprotocol.io/retail`
   - **Advantages**: Always available, managed by Beckn Protocol organization
   - **Disadvantages**: External dependency, no control over availability

### Kubernetes Configuration

- **Namespace**: `beckn-spec`
- **Service Type**: LoadBalancer (public-facing)
- **Port**: 80 (external) → 7860 (container)
- **Resource Limits**: 1Gi memory, 500m CPU
- **Replicas**: 1

## 🧪 Usage

1. **Open the web interface**
2. **Paste your Beckn JSON payload** in the text area
3. **Click "Validate Payload"**
4. **Review the validation results**

### Example Payload

```json
{
  "context": {
    "domain": "local-retail",
    "action": "search",
    "version": "1.1.0",
    "bap_id": "example.bap.com",
    "bap_uri": "https://example.com",
    "transaction_id": "1234567890",
    "message_id": "0987654321",
    "timestamp": "2023-11-06T09:41:09.673Z"
  },
  "message": {
    "intent": {
      "item": {
        "descriptor": {
          "name": "Product Name"
        }
      }
    }
  }
}
```

## 🔍 Troubleshooting

### Common Issues

1. **Environment variables not set**
   - Ensure API keys are properly configured
   - Check Kubernetes secrets exist

2. **MCP server not responding**
   - Verify subprocess environment variables
   - Check MCP server logs

3. **Validation service unreachable**
   - Confirm `BECKN_VALIDATOR_URL` is correct
   - Check network connectivity

### Debug Commands

```bash
# Check pod status
kubectl get pods -n beckn-spec

# View application logs
kubectl logs <pod-name> -n beckn-spec

# Check environment variables
kubectl exec <pod-name> -n beckn-spec -- env | grep API_KEY

# Describe deployment
kubectl describe deployment spec-validator-deployment -n beckn-spec
```

## 🛠️ Development

### Adding New Features

1. **Modify validation logic** in `mcp_server.py`
2. **Update UI components** in `ui.py`
3. **Enhance AI agent** in `my_agent.py`
4. **Test locally** with `uv run ui.py`
5. **Rebuild and deploy** with `./build-and-push.sh`

### Code Style

- Follow Python PEP 8 guidelines
- Use type hints where appropriate
- Add docstrings for functions and classes
- Keep functions focused and small

## 📊 Performance

- **Image Size**: ~200MB (optimized)
- **Startup Time**: ~30 seconds
- **Memory Usage**: 512Mi-1Gi
- **CPU Usage**: 250m-500m

## 🔒 Security

- **API keys** stored as Kubernetes secrets
- **No sensitive data** in container images
- **Network isolation** with internal service communication
- **Resource limits** to prevent abuse

## 📄 License

[Add your license information here]

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📞 Support

For issues and questions:
- Create an issue in the repository
- Contact the development team
- Check the troubleshooting section above

---

**Built with ❤️ for the Beckn ecosystem**
