import {useState, useEffect} from "react";

import Card from '@mui/material/Card';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';

import Todo from "@/types/Todo";
import { postFetch } from "../../functions/fetch";


export default function TodoCard({
	id,
	title,
	description,
	done,
	date 
} : Todo) {
	const [done_loc, setDone] = useState<boolean>(done);
	useEffect(() => {
		postFetch("/edit", JSON.stringify({
			"id": id,
			"done": Boolean(done_loc)
		}));
	}, [done_loc]);
	return (
		<Card sx={{ minWidth: 275 }}>
			<CardContent>
				<Typography variant="h5" component="div">
					{title}
				</Typography>
				<Typography variant="body2">
					{description}
				</Typography>
				<Typography sx={{ mb: 1.5 }} color="text.secondary">
					{date}
				</Typography>
			</CardContent>
			<CardActions>
				<Button size="small" onClick={() => setDone(!done_loc)}>
					{ done_loc ? "まだ" : "できた" }
				</Button>
			</CardActions>
		</Card>
	);
}