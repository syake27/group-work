document.addEventListener('DOMContentLoaded', () => {
    const amounts = [100, 200, 300, 400, 500];
    let index = 0;
    let intervalId = null;
    let isRunning = false;

    const rouletteBtn = document.getElementById('roulette-btn');
    const amountDisplay = document.getElementById('amount');

    rouletteBtn.addEventListener('click', () => {
        console.log('ボタン押された'); // ← これが出るか確認
        if (isRunning) return;
        isRunning = true;

        intervalId = setInterval(() => {
            index = (index + 1) % amounts.length;
            amountDisplay.textContent = amounts[index];
            console.log('更新中:', amounts[index]); // ← ここも確認
        }, 100);

        setTimeout(() => {
            clearInterval(intervalId);
            const randomAmount = Math.floor(Math.random() * 1000) + 1;
            amountDisplay.textContent = `${randomAmount}円`;
            console.log('最終:', randomAmount);
            isRunning = false;
        }, 3000);
    });


});
e