import { Chatbot } from './components/Chatbot'

const App = () => {
  return (
    <div style={{ 
      minHeight: '100vh', 
      background: 'linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)',
      padding: '20px',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center'
    }}>
      <Chatbot />
    </div>
  )
}

export default App