// frontend/app/page.tsx
'client';

import { useState, useEffect } from 'react';

export default function Dashboard() {
  const [ledger, setLedger] = useState({
    account_id: 'USFEX-CORE-01',
    balance: 142500.00,
    currency: 'USD',
    status: 'CONNECTING...'
  });

  useEffect(() => {
    // Connect to FastAPI Server-Sent Events stream
    const eventSource = new EventSource('http://localhost:8000/api/financial/stream');
    
    eventSource.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setLedger(data);
    };

    return () => {
      eventSource.close();
    };
  }, []);

  return (
    <main style={{ padding: '2rem', backgroundColor: '#0f172a', color: '#f8fafc', minHeight: '100vh', fontFamily: 'sans-serif' }}>
      <h1 style={{ fontSize: '2rem', marginBottom: '0.5rem' }}>UriesmoothAI-videomini</h1>
      <p style={{ color: '#94a3b8', marginBottom: '2rem' }}>Real-time Financial Ledger & Voice Agent Matrix</p>
      
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '1.5rem' }}>
        <div style={{ background: '#1e293b', padding: '1.5rem', borderRadius: '8px', border: '1px solid #334155' }}>
          <h3>Account Status</h3>
          <p style={{ fontSize: '1.25rem', fontWeight: 'bold', color: '#38bdf8' }}>{ledger.status}</p>
          <p style={{ color: '#94a3b8', fontSize: '0.9rem' }}>Account ID: {ledger.account_id}</p>
        </div>

        <div style={{ background: '#1e293b', padding: '1.5rem', borderRadius: '8px', border: '1px solid #334155' }}>
          <h3>Live Balance</h3>
          <p style={{ fontSize: '2rem', fontWeight: 'bold', color: '#4ade80' }}>
            ${ledger.balance.toLocaleString()} <span style={{ fontSize: '1rem', color: '#94a3b8' }}>{ledger.currency}</span>
          </p>
        </div>
      </div>
    </main>
  );
}
