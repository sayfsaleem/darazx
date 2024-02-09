(function () {
    // Your web app's Firebase configuration
    var firebaseConfig = {
      apiKey: "AIzaSyB77UvNq3sV4NE2ihYvaiKkdeUDuim4qPI",
      projectId: "darazmall-6b211",
    };
    // Initialize Firebase
    firebase.initializeApp(firebaseConfig);

    const db = firebase.firestore();

    // Get Elements
    const txtEmail = document.getElementById("txtEmail");
    const txtPassword = document.getElementById("txtPassword");
    const firstName = document.getElementById("firstName"); // Add HTML elements for firstname, lastname, and phone number
    const lastName = document.getElementById("lastName");
    const phoneNumber = document.getElementById("phoneNumber");
    const btnSignup = document.getElementById("btnSignup");

    // Add Signup Event
    btnSignup.addEventListener("click", async (e) => {
      // Get email, password, firstname, lastname, and phone number
      const email = txtEmail.value;
      const password = txtPassword.value;
      const userFirstName = firstName.value;
      const userLastName = lastName.value;
      const userPhoneNumber = phoneNumber.value;

      const auth = firebase.auth();

      try {
        // Signup with Firebase Auth
        const userCredential = await auth.createUserWithEmailAndPassword(
          email,
          password
        );
        const user = userCredential.user;

        // Add user data to Firestore
        const userRef = db.collection("users");
        await userRef.doc(user.uid).set({
          email: user.email,
          firstName: userFirstName,
          lastName: userLastName,
          phoneNumber: userPhoneNumber,
          // Add other user data fields as needed
        });

        //   alert("Signup Successful :)");
        Swal.fire({
          icon: "success",
          title: "Signup Successful!",
          text: "You have successfully signed up.",
          confirmButtonColor: "#2000d1",
        });
        setTimeout(() => {
          window.location.href = "login.html";
        }, 2000);
      } catch (err) {
        //   alert(err.message);
        Swal.fire({
          icon: "error",
          title: "Signup Failed",
          text: err.message,
        });
      }
    });
  })();
