// Theaters.tsx

import React from 'react';

interface Theater {
  id: number;
  name: string;
  location: string;
}

interface TheatersProps {
  theaters: Theater[];
}

const Theaters: React.FC<TheatersProps> = ({ theaters }) => {
  return (
    <div>
      <h2>Available Theaters</h2>
      <ul>
        {theaters.map((theater) => (
          <li key={theater.id}>
            <p>Name: {theater.name}</p>
            <p>Location: {theater.location}</p>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Theaters;