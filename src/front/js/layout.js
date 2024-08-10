import React, { useEffect, useContext } from "react";
import { BrowserRouter, Route, Routes, Navigate } from "react-router-dom";
import ScrollToTop from "./component/scrollToTop";
import Signup from "./pages/signup";
import Login from "./pages/login";
import Private from "./pages/private";  // Asegúrate de que esta ruta sea correcta
import injectContext, { Context } from "./store/appContext";
import Navbar from "./component/navbar";
import { Footer } from "./component/footer";

const Layout = () => {
    const { actions } = useContext(Context);
    const basename = process.env.BASENAME || "";

    useEffect(() => {
        actions.syncTokenFromSessionStorage();
    }, [actions]);

    return (
        <div>
            <BrowserRouter basename={basename}>
                <ScrollToTop>
                    <Navbar />
                    <Routes>
                        <Route path="/signup" element={<Signup />} />
                        <Route path="/login" element={<Login />} />
                        <Route path="/private" element={<Private />} /> {/* Usar Private */}
                        <Route path="*" element={<Navigate to="/login" />} />
                    </Routes>
                    <Footer />
                </ScrollToTop>
            </BrowserRouter>
        </div>
    );
};

export default injectContext(Layout);
