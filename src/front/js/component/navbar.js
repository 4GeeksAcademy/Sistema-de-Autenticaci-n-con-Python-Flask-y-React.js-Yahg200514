
import React, { useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import { Context } from '../store/appContext';

const Navbar = () => {
    const { actions } = useContext(Context);
    const navigate = useNavigate();

    const handleLogout = () => {
        actions.logout();
    };

    return (
        <nav>
            <button onClick={handleLogout}>Cerrar Sesion</button>
        </nav>
    );
};

export default Navbar;

