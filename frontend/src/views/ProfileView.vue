<template>

<div>

<h1>

Profile

</h1>


<button @click="logout">

Logout

</button>


</div>

</template>


<script setup>

import {useRouter}
from "vue-router";


const router =
useRouter();



function logout(){

localStorage.removeItem(
"token"
);


router.push(
"/"
);

}


</script>