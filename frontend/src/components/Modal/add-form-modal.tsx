import SendIcon from '@mui/icons-material/Send';
import { Button, TextField } from "@mui/material";

import { postFetch } from "../../functions/fetch";
import Modal from './modal';
import { FormEventHandler } from "react";


export default function AddFormModal ({
	isShowModal,
	setShowModal,
	afterAddTodo
}:{
	isShowModal: boolean,
	setShowModal: (flag: boolean) => void,
	afterAddTodo: () => void
}) {
	const addFormEventHandler: FormEventHandler<HTMLFormElement> = async (event) => {
		event.preventDefault();
		const form = new FormData(event.currentTarget);
		const title = form.get("title");
		const description = form.get("description");
		const date = form.get("date")?.toString();

		// データ送信
		const res = await postFetch("/create", JSON.stringify({
			"title": title,
			"description": description,
			"date": date?.replace(/-/g, "/"),
		}));

		if (!res.ok) {
			alert("追加に失敗しました");
		}

		setShowModal(false);
		afterAddTodo();
	}
	
	return (
		<>
			<Modal title="Todoの追加" isShowModal={isShowModal} closeModal={setShowModal}>
				<form onSubmit={addFormEventHandler}>
					<TextField
						required
						id="add-title"
						name="title"
						label="タイトル"
						variant="standard"
						margin="normal"
						sx={{
							width: "100%"
						}}
					/><br />
					<label>期限</label><br />
						<TextField
							required
							id="add-date"
							name="date"
							type="date"
							sx={{
								width: 200
							}}
							margin="none"
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
					/><br />
					<Button
						type="submit"
						endIcon={<SendIcon />}
						sx={{
							left: "auto"
						}}
					>
						Send
					</Button>
				</form>
			</Modal>
		</>
	)
}