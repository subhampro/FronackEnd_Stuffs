const fakeDataApi = (url) => {
	return new Promise((accept,reject)=>{
		const timeout = Math.ceil(Math.random() * 3000)
		console.log(`Timeout Number Is : ${timeout}`)
		setTimeout(()=>{
			if (timeout > 1500) {
				accept(`Congratulations you get the data From website ${url}`);
			} else {reject("Server Connection Failed !")}
		},timeout)
	})
}

// fakeDataApi("https://data.com/api/page1")
// 	.then((data)=>{
// 		console.log("Connection Established!")
// 		console.log(data)
// 			fakeDataApi("https://data.com/api/page2")
// 				.then((data)=>{
// 					console.log("Connection Established to Page 2!")
// 					console.log(data)
// 						fakeDataApi("https://data.com/api/page3")
// 							.then((data)=>{
// 								console.log("Connection Established to Page 3!")
// 								console.log(data)
// 									fakeDataApi("https://data.com/api/page4")
// 										.then((data)=>{
// 											console.log("Connection Established to Page 4!")
// 											console.log(data)
// 										})
// 										.catch((err)=>{
// 											console.log("Yooo ! Sad ...... You dont get the data!")
// 											console.log(err)	
// 										})
// 							})
// 							.catch((err)=>{
// 								console.log("Yooo ! Sad ...... You dont get the data!")
// 								console.log(err)	
// 							})
// 				})
// 				.catch((err)=>{
// 					console.log("Yooo ! Sad ...... You dont get the data!")
// 					console.log(err)	
// 				})
// 	})
// 	.catch((err)=>{
// 	console.log("Yooo ! Sad ...... You dont get the data!")
// 	console.log(err)	
// 	})



fakeDataApi('wwww.google.com/Api/pg1')
	.then((data)=>{
		console.log("Connection Established to Page 1!")
		console.log(data)
			return fakeDataApi('wwww.google.com/Api/pg2')
	})
	.then((data)=>{
		console.log("Connection Established to Page 2!")
		console.log(data)
			return fakeDataApi('wwww.google.com/Api/pg3')
	})
	.then((data)=>{
		console.log("Connection Established to Page 3!")
		console.log(data)
			return fakeDataApi('wwww.google.com/Api/pg4')
	})
	.then((data)=>{
		console.log("Connection Established to Page 4!")
		console.log(data)
	})

	.catch((err)=>{
		console.log("Yooo ! Sad ...... You dont get the data!")
		console.log(err)	
	})