export async function updateFetch (
	options: string
) {
	return await fetch("http://localhost:8000/edit", {
		"method": "post",
		"headers": {
			"Content-Type": "application/json"
		},
		"body" : options
	})
}