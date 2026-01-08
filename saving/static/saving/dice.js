document.addEventListener('DOMContentLoaded', () => {
    const guessSelect = document.getElementById('guess');
    const diceResult = document.getElementById('dice-result');
    const moneyDisplay = document.getElementById('money');
    const diceBtn = document.getElementById('dice-btn');

    let isRolling = false;

    diceBtn.addEventListener('click', () => {
        if (isRolling) return; // 連打防止
        isRolling = true;

        diceBtn.textContent = '転がっています…';
        moneyDisplay.textContent = '---';

        let speed = 60;
        let rollCount = 0;

        function rollDice() {
            const dice = Math.floor(Math.random() * 6) + 1;
            diceResult.textContent = `🎲 ${dice}`;
            rollCount++;

            speed += 15;

            if (rollCount < 20) {
                setTimeout(rollDice, speed);
            } else {
                // 完全停止処理
                const guess = Number(guessSelect.value);
                let money;

                if (dice === guess) {
                    money = dice * 200;
                } else {
                    money = 100;
                }

                moneyDisplay.textContent = `${money}円`;
                diceBtn.textContent = 'サイコロを振る';
                isRolling = false;
            }
        }

        rollDice();
    });
});
