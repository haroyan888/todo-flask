// react
import {useState, useEffect} from "react";

// components
import Card from '@mui/material/Card';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
// icons
import CheckIcon from '@mui/icons-material/Check';

// self components
import Todo from "@/types/Todo";
import { postFetch } from "../../functions/fetch";
import DetailTodoModal from "../Modal/detail-modal";


export default function TodoCard({
	todo,
	afterEditTodo
} : {
	todo:Todo,
	afterEditTodo: () => void
}) {
	// Todoを行ったかどうかを表す
	const [doneLoc, setDone] = useState<boolean>(todo.done);
	// Todoの詳細モーダルの開閉状態を表す
	const [isShowDetailTodo, setShowDetailTodo] = useState<boolean>(false);
	useEffect(() => {
		postFetch("/edit", JSON.stringify({
			"id": todo.id,
			"done": Boolean(doneLoc)
		}));
	}, [doneLoc]);
	return (
		<>
			<Card 
				sx={{ 
					minWidth: 275,
					backgroundColor: "#f5f5f5"
				}}
			>
				<CardContent>
					<Typography variant="h5" component="div">
						{todo.title}
						{doneLoc ? (
								<CheckIcon 
									sx={{ ml: 2 }}
									color="success"
								/>
							) : undefined
						}
					</Typography>
					<Typography variant="body2">
						{todo.description === undefined ? todo.description : todo.description.length < 20 ? todo.description : todo.description.slice(0, 20) + "..." }
					</Typography>
					<Typography sx={{ mb: 1.5 }} color="text.secondary">
						{todo.date}
					</Typography>
				</CardContent>
				<CardActions>
					<Button 
						size="small" 
						color={doneLoc ? "error" : "success"}
						variant="contained"
						onClick={() => setDone(!doneLoc)}
					>
						{ doneLoc ? "まだ" : "できた" }
					</Button>
					<Button variant="contained" onClick={() => setShowDetailTodo(true)}>
						詳細
					</Button>
				</CardActions>
			</Card>
			<DetailTodoModal 
				todo={todo}
				isShowModal={isShowDetailTodo}
				setShowModal={setShowDetailTodo}
				afterEditTodo={afterEditTodo}
			/>
		</>
	);
}