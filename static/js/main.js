document.addEventListener('DOMContentLoaded', function() {
    const dropdowns = document.querySelectorAll('.dropdown');

    dropdowns.forEach(dropdown => {
        dropdown.addEventListener('mouseenter', function() {
            this.querySelector('.dropdown-content').style.display = 'block';
        });

        dropdown.addEventListener('mouseleave', function() {
            this.querySelector('.dropdown-content').style.display = 'none';
        });
    });
});

document.addEventListener('DOMContentLoaded', function() {
  const dropdowns = document.querySelectorAll('.dropdown');

  dropdowns.forEach(dropdown => {
      dropdown.addEventListener('mouseenter', function() {
          this.querySelector('.dropdown-content-plus').style.display = 'block';
      });

      dropdown.addEventListener('mouseleave', function() {
          this.querySelector('.dropdown-content-plus').style.display = 'none';
      });
  });
});

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('register-form');
    const usernameInput = form.querySelector('#id_username');
    const emailInput = form.querySelector('#id_email');
    const password1Input = form.querySelector('#id_password1');
    const password2Input = form.querySelector('#id_password2');

    form.addEventListener('submit', function(event) {
        if (!form.checkValidity()) {
            event.preventDefault();
            event.stopPropagation();
        }

        form.classList.add('was-validated');
    });

    usernameInput.addEventListener('input', function() {
        if (usernameInput.validity.patternMismatch) {
            usernameInput.setCustomValidity('Username must contain only letters, numbers, and underscores.');
        } else {
            usernameInput.setCustomValidity('');
        }
    });

    emailInput.addEventListener('input', function() {
        if (emailInput.validity.typeMismatch) {
            emailInput.setCustomValidity('Please enter a valid email address.');
        } else {
            emailInput.setCustomValidity('');
        }
    });

    password1Input.addEventListener('input', function() {
        if (password1Input.validity.tooShort) {
            password1Input.setCustomValidity('Password should be at least 6 characters long.');
        } else {
            password1Input.setCustomValidity('');
        }
    });

    password2Input.addEventListener('input', function() {
        if (password2Input.validity.patternMismatch) {
            password2Input.setCustomValidity('Passwords do not match.');
        } else {
            password2Input.setCustomValidity('');
        }
    });
});

document.addEventListener('DOMContentLoaded', function() {
    var calendar = document.getElementById('calendar');
    var date = new Date();
    var year = date.getFullYear();
    var month = date.getMonth();
  
    renderCalendar(year, month);
  
    function renderCalendar(year, month) {
      var firstDay = new Date(year, month, 1);
      var lastDay = new Date(year, month + 1, 0);
      var daysInMonth = lastDay.getDate();
  
      var startDate = new Date(firstDay);
      startDate.setDate(startDate.getDate() - startDate.getDay());
      var endDate = new Date(lastDay);
      endDate.setDate(endDate.getDate() + 6 - endDate.getDay());
      var weeks = [];
  
      while (startDate <= endDate) {
        var week = [];
        for (var i = 0; i < 7; i++) {
          var day = {
            date: startDate.getDate(),
            month: startDate.getMonth(),
            year: startDate.getFullYear()
          };
          week.push(day);
          startDate.setDate(startDate.getDate() + 1);
        }
        weeks.push(week);
      }
  
      var daysList = document.querySelector('.days');
      daysList.innerHTML = '';
  
      weeks.forEach(function(week) {
        var weekRow = document.createElement('ul');
        weekRow.classList.add('week');
        week.forEach(function(day) {
          var dayItem = document.createElement('li');
          dayItem.textContent = day.date;
          dayItem.setAttribute('data-day', day.date);
          dayItem.setAttribute('data-month', day.month + 1); 
          dayItem.setAttribute('data-year', day.year);
          weekRow.appendChild(dayItem);
  
 
          if (hasEvent(day.year, day.month, day.date)) {
            dayItem.classList.add('event-day');
          }
        });
        daysList.appendChild(weekRow);
      });
    }

    function hasEvent(year, month, day) {
      return (year === 2024 && month === 5 && day === 24) || (year === 2024 && month === 5 && day === 26);
    }
  });

const popUpForm = document.getElementById("profilePhotoForm");
var button = document.getElementById("profilePhotoBtn");


button.addEventListener("click", function() {
  popUpForm.style.display = "block";
  button.style.display = "none";
  
});