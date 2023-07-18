import { useState, useEffect } from "react";
import axios from "axios";
import { Modal, Button, Table } from "react-bootstrap";
import "bootstrap/dist/css/bootstrap.min.css";
import classnames from "classnames";

const Login = ({ handleLogin, error}) => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const handleLoginClick = () => {
    (handleLogin(username, password))
  };

  return (
    <div className="container d-flex justify-content-center align-items-center vh-100">
      <div>
        <h2>Login</h2>
        <br />
        <div className="mb-3">
          <label htmlFor="username" className="form-label">
            Username:
          </label>
          <input
            className="form-control"
            type="text"
            id="username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
        </div>
        <div className="mb-3">
          <label htmlFor="password" className="form-label">
            Password:
          </label>
          <input
            className="form-control"
            type="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>
        {error && <p>{error}</p>}
        <button className="btn btn-primary" onClick={handleLoginClick}>
          Login
        </button>
      </div>
    </div>
  );
};

const Cadastros = ({data, showError, selectedItems, DeleteSelectedItems, ItemSelection, showModal}) => {
	return(
			<div>
				<br></br>
				<h2 className="text-center">Exclusão de cadastro</h2>
				<p className={classnames("text-center", showError && "text-danger")}>Selecione os cadastros que serão removidos</p>
				<br></br>
				
				<Table striped bordered>
				  <thead>
					<tr>
					  <th>ID</th>
					  <th>Nome</th>
					  <th>CPF</th>
					  <th>Data de Nascimento</th>
					  <th><img src="https://cdn-icons-png.flaticon.com/512/39/39220.png?w=740&t=st=1689557971~exp=1689558571~hmac=f78d7adedcd64aab755997f00c7235234857f27e5184747ce472ed1d180675f9" alt="delete" width={20} /></th>
					</tr>
				  </thead>
				  <tbody>
					{data.map((item) => (
					  <tr key={item.id}>
						<td>{item.id}</td>
						<td>{item.nome}</td>
						<td>{item.cpf}</td>
						<td>{item.data_nascimento}</td>
						<td>
						  <input
							type="checkbox"
							checked={selectedItems.includes(item.id)}
							onChange={() => ItemSelection(item.id)}
						  />
						</td>
					  </tr>
					))}
				  </tbody>
				</Table>
				
				<div className="d-flex justify-content-between">
				  <Button href="/">Voltar</Button>
				  <Button variant="primary" onClick={DeleteSelectedItems}>
					Excluir
				  </Button>
				</div>
			</div>
	);
}

const ModalDelete = ({showModal, CancelDelete, ConfirmDelete}) => {
	return (
		<Modal show={showModal} onHide={CancelDelete}>
            <Modal.Header closeButton>
				<Modal.Title>Confirmação de Exclusão</Modal.Title>
            </Modal.Header>
            <Modal.Body>
				Tem certeza que deseja excluir os itens selecionados?
            </Modal.Body>
            <Modal.Footer>
				<Button variant="secondary" onClick={CancelDelete}>
					Cancelar
                </Button>
				<Button variant="primary" onClick={ConfirmDelete}>
					Confirmar
                </Button>
            </Modal.Footer>
        </Modal>
	);
}

const ModalAlert = ({showAlert, CancelAlert}) => {
	return(
		<Modal show={showAlert} onHide={CancelAlert}>
			<Modal.Header closeButton></Modal.Header>
			<Modal.Body>Exclusão bem sucedida!</Modal.Body>
			<Modal.Footer>
				<Button variant="primary" onClick={CancelAlert}>OK</Button>
			</Modal.Footer>
		</Modal>	
	);
}

function App() {
  const [authenticated, setAuthenticated] = useState(false);
  const [error, setError] = useState("");
  const [data, setData] = useState([]);
  const [showError, setShowError] = useState(false);
  const [selectedItems, setSelectedItems] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [showAlert, setShowAlert] = useState(false);

  const handleLogin = (username, password) => {
    const credentials = btoa(`${username}:${password}`);

    axios
      .get("http://0.0.0.0:8000/delete", {
        headers: {
          Authorization: `Basic ${credentials}`,
        },
      })
      .then((response) => {
        const data = response.data;
        setData(data);
        setAuthenticated(true);
        setError("");
      })
      .catch((error) => {
        console.error(error);
        setError("Credenciais inválidas");
      });
  };

  const DeleteSelectedItems = () => {
    if (selectedItems.length > 0) {
      setShowModal(true);
    } else {
      setShowError(true); // Mostrar erro se nenhum item estiver selecionado
    }
  };

  const ItemSelection = (itemId) => {
    if (selectedItems.includes(itemId)) {
      setSelectedItems(selectedItems.filter((id) => id !== itemId));
    } else {
      setSelectedItems([...selectedItems, itemId]);
    }
  };

  const ConfirmDelete = () => {
    axios
      .post("http://0.0.0.0:8000/delete", { selectedItems })
      .then((response) => {
        setShowModal(false);
        setShowAlert(true);
        const filteredData = data.filter((item) => !selectedItems.includes(item.id));
        const updatedData = filteredData.map((item, index) => {
          return {
            ...item,
            id: index + 1, // Atribuir o ID corrigido com base no novo índice
          };
        });
        setData(updatedData);
      })
      .catch((error) => {
        console.error(error);
      });
  };

  const CancelDelete = () => {
    setShowModal(false);
  };

  const CancelAlert = () => {
    setShowAlert(false);
  };


  return (
    <div className="vh-100 vw-100">
      <nav className="navbar navbar-light bg-light">
        <div className="container-fluid">
            <a className="navbar-brand" href="/">/home</a>
        </div>
      </nav>
      {!authenticated && (
        <Login handleLogin={handleLogin} error={error}/>
      )}

      {authenticated && (
        <div className="vh-100 d-flex justify-content-center">
		
          <Cadastros data={data} showError={showError} selectedItems={selectedItems} DeleteSelectedItems={DeleteSelectedItems} ItemSelection={ItemSelection} />
          <ModalDelete showModal={showModal} ConfirmDelete={ConfirmDelete} CancelDelete={CancelDelete}/>
          <ModalAlert showAlert={showAlert} CancelAlert={CancelAlert} />
        </div>
      )}
    </div>
  );
}

export default App;
