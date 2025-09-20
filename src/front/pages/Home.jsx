import React, { useEffect, useState } from "react"
import { useNavigate } from "react-router-dom";

export const Home = () => {

	const backendUrl = import.meta.env.VITE_BACKEND_URL

	const [isLogin, setIsLogin] = useState(false);
	const [username, setUsername] = useState("");
	const [password, setPassword] = useState("");
	const navigate = useNavigate();

	const handleSubmit = async (e) => {
		e.preventDefault();

		try {
			let credentials = {
				username,
				password
			};

			if (isLogin) {

				let response = await fetch(backendUrl + "api/login", {
					method: "POST",
					headers: { "Content-type": "application/json" },
					body: JSON.stringify(credentials),
				});

				if (!response.ok) {
					alert("Error en login. Verifica tus credenciales.");
					return;
				}

				let data = await response.json();
				localStorage.setItem("token", data.token);
				localStorage.setItem("user", JSON.stringify(data.user));
				alert("Login exitoso ✅");
				console.log("Login:", data);
				navigate("/mytasks")

			} else {
				let response = await fetch(backendUrl + "api/register", {
					method: "POST",
					headers: { "Content-type": "application/json" },
					body: JSON.stringify(credentials),
				});

				if (!response.ok) {
					alert("Error al registrar. Intenta de nuevo.");
					return;
				}

				alert("Registro exitoso 🎉 Ahora inicia sesión");
				setIsLogin(true); 
			}
		} catch (err) {
			alert("Error de conexión. Inténtalo otra vez.");
			console.error(err);
		}
	};

	return (
		<div className="container d-flex justify-content-center align-items-center mt-5">
			<div className="card shadow-lg p-4" style={{ width: "350px" }}>
				<h3 className="text-center mb-4">
					{isLogin ? "Iniciar Sesión" : "Registrarse"}
				</h3>
				<form onSubmit={handleSubmit}>
					<div className="mb-3">
						<label className="form-label">Usuario</label>
						<input
							type="text"
							className="form-control"
							value={username}
							onChange={(e) => setUsername(e.target.value)}
							placeholder="Ingresa tu usuario"
							required
						/>
					</div>
					<div className="mb-3">
						<label className="form-label">Contraseña</label>
						<input
							type="password"
							className="form-control"
							value={password}
							onChange={(e) => setPassword(e.target.value)}
							placeholder="Ingresa tu contraseña"
							required
						/>
					</div>
					<button type="submit" className="btn btn-primary w-100">
						{isLogin ? "Entrar" : "Registrar"}
					</button>
				</form>
				<div className="text-center mt-3">
					<button
						type="button"
						className="btn btn-link"
						onClick={() => setIsLogin(!isLogin)}
					>
						{isLogin
							? "¿No tienes cuenta? Regístrate"
							: "¿Ya tienes cuenta? Inicia sesión"}
					</button>
				</div>
			</div>
		</div>
	);
}; 