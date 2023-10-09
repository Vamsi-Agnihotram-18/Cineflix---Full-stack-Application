import React, { useState } from 'react';

const InputField = ({ label, type, value, onChange }) => (
  <label>
    {label}:
    <input type={type} value={value} onChange={onChange} />
  </label>
);

const SignUp: React.FC = () => {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [errors, setErrors] = useState({});
  const [isLoading, setIsLoading] = useState(false);

  const validateForm = () => {
    const newErrors = {};
    if (!username) newErrors.username = 'Username is required';
    if (!email.includes('@')) newErrors.email = 'Enter a valid email';
    if (password.length < 6) newErrors.password = 'Password must be at least 6 characters';
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSignUp = (event) => {
    event.preventDefault();
    if (!validateForm()) return;
    setIsLoading(true);
    console.log('Sign up with:', { username, email, password });
    // Add your sign-up logic here
    setIsLoading(false);
  };

  return (
    <div>
      <h2>Sign Up</h2>
      <form onSubmit={handleSignUp}>
        <InputField label="Username" type="text" value={username} onChange={(e) => setUsername(e.target.value)} />
        {errors.username && <p>{errors.username}</p>}
        <InputField label="Email" type="email" value={email} onChange={(e) => setEmail(e.target.value)} />
        {errors.email && <p>{errors.email}</p>}
        <InputField label="Password" type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
        {errors.password && <p>{errors.password}</p>}
        <button type="submit" disabled={isLoading}>{isLoading ? 'Signing Up...' : 'Sign Up'}</button>
      </form>
    </div>
  );
};

export default SignUp;
