import React, { useEffect, useContext } from "react";
import { useNavigate } from "react-router-dom";
import { Context } from "../store/appContext";

const Private = ({ children }) => {
    const { store } = useContext(Context);
    const navigate = useNavigate();

    useEffect(() => {
        const token = store.token || sessionStorage.getItem("token");
        if (!token) {
            navigate("/login");
        }
    }, [store.token, navigate]);

    // Verifica si el token existe, de lo contrario redirige o muestra un contenido de carga
    if (!store.token && !sessionStorage.getItem("token")) {
        return <div>Loading...</div>; // Puedes cambiar esto a un componente de carga o un mensaje
    }

    return (
        <div>
            {children || <p>Contenido Privado</p>}
        </div>
    );
};

export default Private;
