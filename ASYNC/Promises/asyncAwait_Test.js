async function fetchData() {
    return new Promise((resolve,reject)=>{ setTimeout(() => {
            resolve(455);
        }, 2000);
    })
}

async function processData() {
    console.log('Processing data...');
    console.log('Waiting for data...');
    console.log('Fetching data...');
    const data = await fetchData();
    console.log('Data fetched:', data);
    console.log('Data processed successfully');
    return data;
    // return Promise.resolve('Data processed successfully');
    // return Promise.reject('Error processing data');
}   

processData()