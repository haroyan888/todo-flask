import {useState, useEffect} from "react";
import AddIcon from '@mui/icons-material/Add';
import ClearIcon from '@mui/icons-material/Clear';
import SendIcon from '@mui/icons-material/Send';
import { Button, IconButton } from "@mui/material";

import './App.css'
import TodoCard from './components/Todo/Todo'
import Todo from './types/Todo';

function App() {
  // Todoの取得に関する処理
  const [todos, setTodos] = useState([]);
  useEffect(() => {
    fetch("http://localhost:8000/api/")
      .then((res) => res.json()) 
      .then ((json) => setTodos(json["todos"]))
      .catch(() => alert("データの取得に失敗しました"))
  }, [])

  // Todoの追加用モーダルに関する処理
  const [isShowModal, setShowModal] = useState<boolean>(false);

  return (
    <>
      {todos !== undefined ?
        todos.map((element: Todo) => {
          return (
            <div key={element["id"]} className="m-10">
              <TodoCard 
                id={element["id"]} 
                title={element["title"]}
                description={element["description"]}
                done={element["done"]}
                date={element["date"]}
              />
            </div>
          )
        }) : "Todoはありません"}
      
      {/* Todoを追加するモーダル */}
      <div className="fixed right-10 bottom-10">
        <Button 
          variant="contained"
          onClick={() => setShowModal(true)}
          endIcon={<AddIcon />}
        >
          Add
        </Button>
      </div>
      {isShowModal ? (
        <>
          <div className="overlay" onClick={() => setShowModal(false)} />
          <div className="modal-container">
            <div className="modal-content">
              <div className="modal-content_header flex items-center justify-between mb-3">
                <h1>Todoの追加</h1>
                <IconButton 
                  onClick={() => setShowModal(false)}
                  className="right-0"
                >
                  <ClearIcon />
                </IconButton>
              </div>
              <div className="modal-content_body m-3">
                <Button
                  onClick={() => {
                    setShowModal(false);
                    setTodos([]);
                  }}
                  endIcon={<SendIcon />}
                >
                  Send
                </Button>
              </div>
            </div>
          </div>
        </>
        ): null}
    </>
  )
}

export default App
