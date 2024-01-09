import React from 'react';
import { BrowserRouter as Router, Route } from 'react-router-dom';
import Login from './components/Login';

class App extends React.Component {
    render() {
        return (
            <Router>
                <Route path="/login" component={Login} />
                {/* Other routes here */}
            </Router>
        );
    }
}

export default App;