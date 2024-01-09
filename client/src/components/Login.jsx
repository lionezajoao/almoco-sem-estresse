import React from 'react';

class Login extends React.Component {
    handleLogin = (event) => {
        event.preventDefault();
        // Handle login here
    }

    render() {
        return (
            <form onSubmit={this.handleLogin}>
                <input type="text" placeholder="Username" />
                <input type="password" placeholder="Password" />
                <input type="submit" value="Login" />
            </form>
        );
    }
}

export default Login;