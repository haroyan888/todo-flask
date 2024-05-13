import { Button } from "@mui/material"

import { postFetch } from "../../functions/fetch";
import Modal from "./modal"

import type Todo from "@/types/Todo";

export default function DeleteTodoModal ({
	afterDeleteTodo,
	isShowModal,
	setShowModal,
	todo
} : {
	afterDeleteTodo: () => void,
	isShowModal: boolean,
	setShowModal: (flag: boolean) => void,
	todo: Todo
}) {
	const deleteTodoHandler = () => {
		(async () => {
			const res = await postFetch("/delete", JSON.stringify({
				"id": todo.id
			}));
			if (!res.ok) {
				alert("削除に失敗しました");
			}
			setShowModal(false);
			afterDeleteTodo();
		})();
	}

	return (
		<Modal
			title="Todoの削除"
			isShowModal={isShowModal}
			closeModal={() => {
				setShowModal(false);
			}}
		>
			<Button onClick={deleteTodoHandler}>削除</Button>
		</Modal>
	)
}