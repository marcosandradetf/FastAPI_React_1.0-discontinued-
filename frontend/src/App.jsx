import { useState, useEffect } from "react";
import axios from "axios";
import { Modal, Button, Table } from "react-bootstrap";
import "bootstrap/dist/css/bootstrap.min.css";
import classnames from "classnames";

const Nav_bar = () => {
  return (
    <nav className="navbar navbar-light bg-secondary border-bottom border-black">
      <div className="container-fluid">
          <a className="navbar-brand text-light" href="/">/home</a>
      </div>
    </nav>
  );
}

const Login = ({ handleLogin, error}) => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const FormSubmit = (e) => {
    e.preventDefault();
    handleLoginClick();
  }

  const handleLoginClick = () => {
    (handleLogin(username, password))
  };

  return (
    <div>
      <div className="mx-5 my-5 pb-5">
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
        <form onSubmit={FormSubmit} className="mb-3">
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
        </form>
        {error && <p>{error}</p>}
        <button className="btn btn-primary" onClick={handleLoginClick}>
          Login
        </button>

      </div>
    </div>
  );
};

const Cadastros = ({data, showError, selectedItems, DeleteSelectedItems, ItemSelection}) => {
  const [searchValue, setSearchValue] = useState("");
  
  const PesquisaCad = (e) => {
    setSearchValue(e.target.value);
  };
  
  const FiltroCad = searchValue ? data.filter(
    (item) => item.nome.toLowerCase().includes(
      searchValue.toLowerCase())): data;

  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 20; // Defina a quantidade de itens a serem exibidos por página
    
  // Obtenha os itens a serem exibidos na página atual com base no estado currentPage
  const indexOfLastItem = currentPage * itemsPerPage;
  const indexOfFirstItem = indexOfLastItem - itemsPerPage;
  const currentItems = FiltroCad.slice(indexOfFirstItem, indexOfLastItem);

  // Função para mudar de página
  const paginate = (pageNumber) => setCurrentPage(pageNumber);

  return(
			<div className="d-flex flex-column align-items-center bg-light">
				<h2 className="text-center mt-5">Exclusão de cadastro</h2>
				<p className={classnames("text-center", showError && "text-danger")}>Selecione os cadastros que serão removidos</p>
        <div className="mb-2" style={{width:'auto'}}>
          <input 
            type="text" 
            className="form-control" 
            placeholder="Filtrar Busca:"
            value={searchValue}
            onChange={PesquisaCad}
          />
        </div>
				
				<div className="bg-light table-container">
          <Table striped bordered style={{ width: "auto" }}>
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
            {currentItems.map((item) => (
              <tr key={item.id}>
              <td>{item.id}</td>
              <td>{item.nome}</td>
              <td>{item.cpf}</td>
              <td>{item.data_nascimento}</td>
              <td>
                <input
                className="form-check-input"
                type="checkbox"
                checked={selectedItems.includes(item.id)}
                onChange={() => ItemSelection(item.id)}
                />
              </td>
              </tr>
            ))}
            </tbody>
          </Table>
        </div>
				
				<div 
          className="d-flex justify-content-between bg-light"
          style={{position: 'absolute', bottom:'50px'}}>
				  <Button href="/" className="mx-5">Voltar</Button>
				  <Button className="mx-5" variant="primary" onClick={DeleteSelectedItems}>
					Excluir
				  </Button>
				</div>

        <div style={{position: 'absolute', bottom:'-10px'}}>
          <Pagination
            itemsPerPage={itemsPerPage}
            totalItems={FiltroCad.length}
            currentPage={currentPage}
            paginate={paginate}
          />
        </div>
        

			</div>
	);
}

const Pagination = ({ itemsPerPage, totalItems, currentPage, paginate }) => {
  const pageNumbers = [];

  for (let i = 1; i <= Math.ceil(totalItems / itemsPerPage); i++) {
    pageNumbers.push(i);
  }

  return (
    <nav className="mt-2 bg-light">
      <ul className="pagination">
        {pageNumbers.map((number) => (
          <li key={number} className="page-item">
            <button
              className={
                number === currentPage ? "page-link active" : "page-link"
              }
              onClick={() => paginate(number)}
            >
              {number}
            </button>
          </li>
        ))}
      </ul>
    </nav>
  );
};

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
        const FiltroCad = data.filter((item) => !selectedItems.includes(item.id));
        const updatedData = FiltroCad.map((item, index) => {
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
    <div style={{height:'100vh', width:'100vw'}}>

      <div>
        <Nav_bar />
      </div>

        {!authenticated && (

          <div 
            className="d-flex justify-content-end align-items-end bg-light" 
            style={{height:'calc(100vh - 115px)', width:'100vw'}}>
            <Login handleLogin={handleLogin} error={error}/>
          </div>

        )}
      
        {authenticated && (
          <div 
            className="d-flex justify-content-center bg-light" 
            style={{minHeight:'100vh', height:'auto', width:'100vw'}}>
      
            <Cadastros data={data} showError={showError} selectedItems={selectedItems} DeleteSelectedItems={DeleteSelectedItems} ItemSelection={ItemSelection}/>
            <ModalDelete showModal={showModal} ConfirmDelete={ConfirmDelete} CancelDelete={CancelDelete}/>
            <ModalAlert showAlert={showAlert} CancelAlert={CancelAlert} />
          </div>
        )}



      <div>

        <div className="bg-light text-center text-lg-start border">
          <div className="text-center p-3 text-dark">
            © 2020 Copyright:
            <a className="text-dark" href="https://GitHub.com/marcosandradetf/"> github.com/marcosandradetf</a>
          </div>
        </div>

      </div>
      

    </div>
  );
}

export default App;
