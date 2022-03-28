<template>
  <div style="display: flex; justify-content: center">
    <el-col :span="6" v-loading="isLoading">
      <el-alert
        title="Invalid username/password"
        type="error"
        show-icon
        :style="{ display: showLoginFailed }"
      ></el-alert>
      <el-form :model="loginForm" :rules="rules" ref="loginForm">
        <el-form-item label="Username" prop="username" class="bold-label">
          <el-input v-model="loginForm.username">
            <template #prefix>
              <el-icon><UserFilled /></el-icon>
            </template>
          </el-input>
        </el-form-item>
        <el-form-item label="Password" prop="password" class="bold-label">
          <el-input type="password" v-model="loginForm.password">
            <template #prefix>
              <el-icon><Lock /></el-icon>
            </template>
          </el-input>
        </el-form-item>
        <el-form-item>
          <el-checkbox label="Remember me" v-model="loginForm.rememberMe" />
        </el-form-item>
        <el-form-item>
          <el-button
            type="primary"
            @click="login"
            :disabled="this.isValid"
            style="width: 100%"
          >
            Login
          </el-button>
        </el-form-item>
      </el-form>
    </el-col>
  </div>
</template>

<script>
import { UserFilled, Lock } from "@element-plus/icons-vue";
import UserApi from "@/utilities/network/user";

// user login page
export default {
  name: "LoginPage",
  components: {
    UserFilled,
    Lock,
  },
  data() {
    return {
      loginForm: {
        username: "",
        password: "",
        rememberMe: false,
      },
      rules: {
        username: [
          { required: true, message: "Please input username", trigger: "blur" },
        ],
        password: [
          { required: true, message: "Please input password", trigger: "blur" },
        ],
      },
      isLoading: false,
      isValid: false,
      showLoginFailed: "none",
    };
  },
  methods: {
    login() {
      this.$refs["loginForm"].validate((isValid) => {
        if (isValid) {
          this.isLoading = true;
          this.showLoginFailed = "none";
          UserApi.login(
            this.loginForm.username,
            this.loginForm.password,
            this.loginForm.rememberMe
          ).catch(() => {
            this.isLoading = false;
            this.showLoginFailed = "";
          });
        } else {
          return false;
        }
      });
    },
  },
};
</script>

<style scoped>
.bold-label {
  font-weight: bolder;
}
</style>
