import { Component, ErrorInfo, ReactNode } from 'react';
import { AlertTriangle, RotateCw } from 'lucide-react';

interface Props {
  children: ReactNode;
}

interface State {
  hasError: boolean;
  error: Error | null;
}

export class ErrorBoundary extends Component<Props, State> {
  public state: State = {
    hasError: false,
    error: null,
  };

  public static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('Uncaught render error:', error, errorInfo);
  }

  public render() {
    if (this.state.hasError) {
      return (
        <div
          style={{
            minHeight: '100vh',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            background: 'var(--bg-app)',
            color: 'var(--text-primary)',
            padding: '2rem',
          }}
        >
          <div
            className="card"
            style={{
              maxWidth: '500px',
              width: '100%',
              display: 'flex',
              flexDirection: 'column',
              gap: '1rem',
              textAlign: 'center',
              alignItems: 'center',
            }}
          >
            <AlertTriangle size={40} style={{ color: 'var(--status-danger)' }} />
            <h2>Application Render Error</h2>
            <p style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>
              {this.state.error?.message || 'An unexpected rendering error occurred.'}
            </p>
            <button
              type="button"
              onClick={() => {
                this.setState({ hasError: false, error: null });
                window.location.reload();
              }}
              className="btn btn-primary"
            >
              <RotateCw size={15} /> Reload Application
            </button>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}
