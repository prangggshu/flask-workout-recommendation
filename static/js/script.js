document.getElementById('recommendForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const data = {
        name: document.getElementById('name').value,
        age: document.getElementById('age').value,
        weight: document.getElementById('weight').value,
        height: document.getElementById('height').value,
        goal: document.getElementById('goal').value,
        body_type: document.getElementById('body_type').value,
        fitness_level: document.getElementById('fitness_level').value,
        equipment: document.getElementById('equipment').value,
        body_part: document.getElementById('body_part').value
    };

    const response = await fetch('/recommend', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });

    const result = await response.json();
    document.getElementById('bmi').innerText = `BMI: ${result.bmi}`;
    document.getElementById('bmi-category').innerText = `Category: ${result.category}`;
    document.getElementById('bmi-advice').innerText = result.bmi_advice;
    document.getElementById('diet').innerText = result.diet;

    const workoutContainer = document.getElementById('workout-container');
    workoutContainer.innerHTML = '';
    result.workouts.forEach(workout => {
        workoutContainer.innerHTML += `
            <div class="workout-card">
                <h4>${workout.Title}</h4>
                <p><strong>Type:</strong> ${workout.Type}</p>
                <p><strong>Body Part:</strong> ${workout.BodyPart}</p>
                <p><strong>Equipment:</strong> ${workout.Equipment}</p>
                <p><strong>Level:</strong> ${workout.Level}</p>
                <p>${workout.Desc}</p>
            </div>
        `;
    });
});
