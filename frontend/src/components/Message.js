import React from 'react';

function Message({ sender, content, isCurrentUser }) {
  return (
    <div style={isCurrentUser ? styles.currentUser : styles.otherUser}>
      <strong>{sender}:</strong> {content}
    </div>
  );
}

const styles = {
  currentUser: {
    textAlign: 'right',
    margin: '5px',
    padding: '8px',
    backgroundColor: '#d1e7dd',
    borderRadius: '5px',
  },
  otherUser: {
    textAlign: 'left',
    margin: '5px',
    padding: '8px',
    backgroundColor: '#f8d7da',
    borderRadius: '5px',
  },
};

export default Message;