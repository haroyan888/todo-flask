import { FormEventHandler, useEffect, useState } from "react";
import dayjs from "dayjs";

import { Button, TextField, Typography, IconButton } from "@mui/material";
import DeleteIcon from '@mui/icons-material/Delete';

import { postFetch } from "../../functions/fetch";
import Modal from './modal';
import DeleteTodoModal from "./delete-todo-modal";

import type Todo from "@/types/Todo";

export default function DetailTodoModal ({
	todo,
	isShowModal,
	setShowModal,
	afterEditTodo
}:{
	todo: Todo,
	isShowModal: boolean,
	setShowModal: (flag: boolean) => void,
	afterEditTodo: () => void
}) {
	// 現在の完了の可否
	const [doneLoc, setDone] = useState<boolean>(false);
	// Todoを編集するボタンのトグル
	const [isEditTodo, setEditTodo] = useState<boolean>(false);
	useEffect(() => {
		setEditTodo(false);
	}, [isShowModal]);
	// Todoを削除するモーダルの表示状態
	const [isShowDeleteModal, setShowDeleteModal] = useState<boolean>(false);

	const editFormEventHandler: FormEventHandler<HTMLFormElement> = async (event) => {
		event.preventDefault();
		const form = new FormData(event.currentTarget);
		const title = form.get("title");
		const description = form.get("description");
		const date = form.get("date")?.toString();

		// データ送信
		const res = await postFetch("/edit", JSON.stringify({
			"id": todo.id,
			"title": title,
			"description": description,
			"date": date?.replace(/-/g, "/"),
		}));

		if (!res.ok) {
			alert("編集に失敗しました");
		}

		setShowModal(false);
		afterEditTodo();
	}
	
	return (
		<>
			<Modal
				title="詳細"
				isShowModal={isShowModal}
				closeModal={() => setShowModal(false)}
			>
				<form id="editTodoForm" onSubmit={editFormEventHandler}>
					{isEditTodo ? (
						<div className="form-field">
							<TextField
								required
								id="edit-title"
								name="title"
								label="タイトル"
								variant="standard"
								margin="normal"
								sx={{
									width: "100%"
								}}
								defaultValue={todo.title}
							/><br />
							<label>期限</label><br />
								<TextField
									required
									id="edit-date"
									name="date"
									type="date"
									sx={{
										width: 200
									}}
									margin="none"
									defaultValue={dayjs(todo.date.split(" ")[0]).format("YYYY-MM-DD")}
								/>
							<br />
							<TextField
								id="add-description"
								name="description"
								label="説明"
								multiline
								minRows="10"
								margin="normal"
								sx={{
									width: "100%"
								}}
								defaultValue={todo.description}
							/><br />
						</div>
					) : (
							<div className="todo-detail">
								<Typography variant="h1" sx={{fontSize:35}}>{todo.title}</Typography>
								<Typography variant="body1" sx={{mt:1.5, mb: 1.5, fontSize: 20}}>{todo.date}</Typography>
								<Typography variant="body1" sx={{mt:1.5, mb: 1.5}}>{todo.description}</Typography>
							</div>
					)}
					<div className="button-container flex gap-5">
						<Button 
							size="small" 
							color={doneLoc ? "error" : "success"}
							variant="contained"
							onClick={() => setDone(!doneLoc)}
						>
							{ doneLoc ? "まだ" : "できた" }
						</Button>
						<IconButton
							sx={{ml: "auto"}}
							onClick={() => {
								setShowDeleteModal(true);
								setShowModal(false);
							}}
						>
							<DeleteIcon />
						</IconButton>
						<Button onClick={() => setEditTodo(!isEditTodo)}>
							{!isEditTodo ? "編集" : "キャンセル"}
						</Button>
						{isEditTodo ? (
							<Button type="submit" variant="contained">適用</Button>
						) : undefined}
					</div>
				</form>
			</Modal>
			{isShowDeleteModal ? (
				<DeleteTodoModal
					afterDeleteTodo={() => {
						setEditTodo(false);
						setShowModal(false);
						afterEditTodo();
					}}
					isShowModal={isShowDeleteModal}
					setShowModal={setShowDeleteModal}
					todo={todo}
				/>
			) : undefined}
		</>
	)
}
