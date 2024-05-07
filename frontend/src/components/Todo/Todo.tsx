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


export default function TodoCard({
	id,
	title,
	description,
	done,
	date 
} : Todo) {
	const [doneLoc, setDone] = useState<boolean>(done);
	useEffect(() => {
		postFetch("/edit", JSON.stringify({
			"id": id,
			"done": Boolean(doneLoc)
		}));
	}, [doneLoc]);
	return (
		<Card 
			sx={{ 
				minWidth: 275,
				backgroundColor: "#f5f5f5"
			}}
		>
			<CardContent>
				<Typography variant="h5" component="div">
					{title}
					{doneLoc ? (
							<CheckIcon 
								sx={{ ml: 2 }}
								color="success"
							/>
						) : undefined
					}
				</Typography>
				<Typography variant="body2">
					{description}
				</Typography>
				<Typography sx={{ mb: 1.5 }} color="text.secondary">
					{date}
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
			</CardActions>
		</Card>
	);
}