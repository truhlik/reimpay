<template>
  <div class="app-header header-shadow">
    <div class="app-header__content">
      <div class="app-header-left">
        <div class="app-header__logo">
          <img src="~/assets/img/logos/color_wide.png" alt="logo" class="only-open">
        </div>
      </div>
      <div class="app-header-right">
<!--        <HeaderUserArea :logged-in="loggedIn" :user="user"/>-->
      </div>
    </div>
  </div>
</template>

<script>
  export default {
    name: 'HeaderSimple',
  };
</script>
