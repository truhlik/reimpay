<template>
  <div class="app-header header-shadow">
    <div class="app-header__mobile-menu">
      <div>
        <button
          :class="{ 'is-active' : isOpen }" @click="toggleMobile('closed-sidebar-open')" class="hamburger close-sidebar-btn hamburger--elastic"
          type="button"
        >
          <span class="hamburger-box">
            <span class="hamburger-inner"></span>
          </span>
        </button>
      </div>
    </div>
    <div class="app-header__content">
      <div class="app-header-left">
      </div>
      <div class="app-header-right">
        <HeaderUserArea :logged-in="loggedIn" :user="user"/>
      </div>
    </div>
  </div>
</template>

<script>

  import { mapActions, mapState } from 'vuex'
  import HeaderUserArea from '~/components/partials/HeaderUserArea'

  export default {
    name: "Header",
    components: { HeaderUserArea },
    computed: {
      ...mapState({
        company: state => state.company.company,
        loggedIn: state => state.auth.loggedIn,
        user: state => state.account.user,
      })
    },
    data() {
      return {
        contactDialog: false,
        isOpen: false,
        isOpenMobileMenu: false,
      }
    },
    methods: {
      ...mapActions({
        getUser: 'account/getUser'
      }),
      // logout: function () {
      //   this.$store.dispatch(AUTH_LOGOUT).then(() => this.$router.push('/login'))
      // },
      toggleMobile(className) {
        const el = document.body
        this.isOpen = !this.isOpen
        this.isOpen ? el.classList.add(className) : el.classList.remove(className)
      },

      toggleMobile2(className) {
        const el = document.body;
        this.isOpenMobileMenu = !this.isOpenMobileMenu
        this.isOpenMobileMenu ? el.classList.add(className) : el.classList.remove(className)
      },
    },
    mounted() {
      this.getUser()
    },
  };
</script>
