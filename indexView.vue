<template>
  <div class="user-center-container">
    <!-- 动态天空背景 -->
    <div class="sky-background">
      <div class="cloud cloud-1"></div>
      <div class="cloud cloud-2"></div>
      <div class="cloud cloud-3"></div>
      <div class="cloud cloud-4"></div>
      <div class="cloud cloud-5"></div>
      <div class="cloud cloud-6"></div>
    </div>

    <!-- 漂浮粒子 -->
    <div class="particles">
      <span v-for="i in 30" :key="i" :style="{ '--i': i }"></span>
    </div>

    <el-card class="user-center-card" :body-style="{ padding: '0px' }">
      <!-- 彩虹装饰 -->
      <div class="rainbow-bar"></div>

      <div class="card-content">
        <!-- 头像区域 -->
        <div class="avatar-section">
          <div class="cloud-avatar-bg">
            <el-avatar :size="120" :src="formData2.avatar ? getAvatarUrl(formData2.avatar) : defaultAvatarUrl" />
          </div>
        </div>

        <!-- 标题区域 -->
        <div class="title-section">
          <h1 class="username">{{ formData2.nickname }}</h1>
          <div class="badge">{{ formData2.role_name }}</div>
        </div>

        <!-- 信息卡片 -->
        <div class="info-cards">
          <div class="info-card" v-for="(item, index) in infoList" :key="index" :style="{ animationDelay: index * 0.1 + 's' }">
            <span class="info-icon">{{ item.icon }}</span>
            <div class="info-text">
              <span class="info-label">{{ item.label }}</span>
              <span class="info-value">{{ item.value }}</span>
            </div>
          </div>
        </div>

        <!-- 按钮区域 -->
        <div class="button-group">
          <el-button type="primary" class="btn-edit" @click="editRow">
            <span class="btn-icon">✏️</span> 编辑信息
          </el-button>
          <el-button type="warning" class="btn-password" @click="changePwd">
            <span class="btn-icon">🔒</span> 修改密码
          </el-button>
        </div>
      </div>

      <!-- 底部装饰 -->
      <div class="grass-decoration"></div>
    </el-card>

    <!-- 编辑个人信息弹窗 -->
    <el-dialog v-model="dialogFormVisible" title="编辑用户信息" style="width: 400px;">
      <el-form :model="formData2" :rules="rules" ref="formRef" label-width="80px">
        <el-upload class="avatar-uploader" action="http://127.0.0.1:8899/api/upload/images/" :show-file-list="false"
          :on-success="handleAvatarSuccess" :before-upload="beforeAvatarUpload"
          style="text-align: center;margin-bottom: 20px;">
          <img v-if="formData2.avatar" :src="getAvatarUrl(formData2.avatar)" class="avatar"
            style="width: 100px;height: 100px;" />
          <i v-else class="el-icon-plus avatar-uploader-icon"></i>
        </el-upload>
        <el-form-item label="用户名:" prop="username">
          <el-input disabled v-model="formData2.username"></el-input>
        </el-form-item>
        <el-form-item label="昵称:" prop="nickname">
          <el-input v-model="formData2.nickname"></el-input>
        </el-form-item>
        <el-form-item label="邮箱:" prop="email">
          <el-input v-model="formData2.email"></el-input>
        </el-form-item>
        <el-form-item label="性别:" prop="gender">
          <el-radio-group v-model="formData2.gender">
            <el-radio label="男">男</el-radio>
            <el-radio label="女">女</el-radio>
            <el-radio label="保密">保密</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="简介:" prop="bio">
          <el-input v-model="formData2.bio"></el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogFormVisible = false">取 消</el-button>
          <el-button type="primary" :loading="editLoading" @click="submitEForm(formRef)">确 定</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 修改密码弹窗 -->
    <el-dialog v-model="passwordVisible" title="修改密码" style="width: 400px;">
      <el-form :model="pwd" :rules="pwdRules" ref="pwdFormRef" label-width="80px">
        <el-form-item label="新密码:" prop="new_password1">
          <el-input v-model="pwd.new_password1" type="password"></el-input>
        </el-form-item>
        <el-form-item label="确认密码:" prop="new_password2">
          <el-input v-model="pwd.new_password2" type="password"></el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="passwordVisible = false">取 消</el-button>
          <el-button type="primary" :loading="resetPsdLoading" @click="savePassword">确 定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, nextTick, computed } from 'vue';
import { ElMessage } from 'element-plus';
import { userEdit, userResetpsd } from '@/api/user/index.js';
import useUserStore from '@/store/modules/user';
import { useRouter } from 'vue-router'

const router = useRouter();
const defaultAvatarUrl = 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png';
const dialogFormVisible = ref(false);
const passwordVisible = ref(false);
const editLoading = ref(false);
const resetPsdLoading = ref(false);

const userStore = useUserStore();
const formData2 = reactive({
  id: userStore.id || '',
  username: userStore.username || '',
  nickname: userStore.nickname || '',
  avatar: userStore.avatar || '',
  email: userStore.email || '',
  gender: userStore.gender || '',
  is_superuser: userStore.is_superuser || '',
  role_name: userStore.role_name || '',
  bio: userStore.bio || ''
});

const infoList = computed(() => [
  { icon: '👤', label: '账号', value: formData2.username },
  { icon: '📧', label: '邮箱', value: formData2.email || '未填写' },
  { icon: '⚧', label: '性别', value: formData2.gender || '未知' },
  { icon: '💼', label: '角色', value: formData2.role_name || '普通用户' },
  { icon: '📝', label: '简介', value: formData2.bio || '这个人很懒，什么都没写~' }
]);

const pwd = reactive({
  new_password1: '',
  new_password2: ''
});

const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  nickname: [{ required: true, message: '请输入昵称', trigger: 'blur' }],
  email: [
    { required: true, message: '请输入邮箱地址', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱地址', trigger: ['blur', 'change'] }
  ],
  gender: [{ required: true, message: '请选择性别', trigger: 'change' }]
};

const pwdRules = {
  new_password1: [{ required: true, message: '请输入新密码', trigger: 'blur' }],
  new_password2: [{ required: true, message: '请再次输入新密码', trigger: 'blur' }]
};

const uploadUrl = 'http://127.0.0.1:8899/upload/';
const getAvatarUrl = (avatar) => {
  if (!avatar || /^(http|https):\/\//.test(avatar)) return avatar;
  return uploadUrl + avatar;
};

const beforeAvatarUpload = (file) => {
  const allowedTypes = ['image/jpeg', 'image/png', 'image/gif'];
  const maxSizeMB = 2;
  const isAllowedType = allowedTypes.includes(file.type);
  const isLtMaxSize = file.size / 1024 / 1024 < maxSizeMB;
  if (!isAllowedType) ElMessage.error(`上传头像图片只能是 ${allowedTypes.join(', ')} 格式!`);
  if (!isLtMaxSize) ElMessage.error(`上传头像图片大小不能超过 ${maxSizeMB}MB!`);
  return isAllowedType && isLtMaxSize;
};

const handleAvatarSuccess = (response) => { formData2.avatar = response.data; };

const formRef = ref(null);
const submitEForm = async (formEl) => {
  if (!formEl) return;
  await formEl.validate(async (valid) => {
    if (valid) {
      editLoading.value = true;
      try {
        const response = await userEdit(formData2);
        if (response.code === 200) {
          Object.assign(formData2, response.data);
          userStore['nickname'] = formData2['nickname'];
          userStore['avatar'] = getAvatarUrl(formData2['avatar']);
          userStore['email'] = formData2['email'];
          userStore['gender'] = formData2['gender'];
          userStore['bio'] = formData2['bio'];
          localStorage.setItem('nickname', userStore['nickname']);
          localStorage.setItem('avatar', userStore['avatar']);
          localStorage.setItem('email', userStore['email']);
          localStorage.setItem('gender', userStore['gender']);
          localStorage.setItem('bio', userStore['bio']);
          ElMessage.success('用户信息修改成功');
        } else {
          ElMessage.error('用户修改失败，请稍后再试' + response.message);
        }
        dialogFormVisible.value = false;
      } catch (error) {
        ElMessage.error('用户信息更新失败');
      } finally {
        editLoading.value = false;
      }
    }
  });
};

const editRow = () => { dialogFormVisible.value = true; };
const changePwd = () => { passwordVisible.value = true; };

const pwdFormRef = ref(null);
const savePassword = async () => {
  pwdFormRef.value.validate(async (valid) => {
    if (valid) {
      if (pwd.new_password1 !== pwd.new_password2) {
        ElMessage.error('两次输入的密码不一致');
        return;
      }
      resetPsdLoading.value = true;
      try {
        const response = await userResetpsd({ new_password1: pwd.new_password1, new_password2: pwd.new_password2 });
        if (response.code === 200) {
          ElMessage.success('密码修改成功，请重新登录！');
          await userStore.useLogout();
          nextTick(() => { router.push('/login'); });
        } else {
          ElMessage.error(`密码修改失败：${response.message || '未知错误'}`);
        }
      } catch (error) {
        ElMessage.error('密码修改失败');
      } finally {
        resetPsdLoading.value = false;
      }
    }
  });
};
</script>

<style scoped>
.user-center-container {
  min-height: calc(100vh - 200px);
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 40px 20px;
  position: relative;
  overflow: hidden;
}

/* 天空背景 */
.sky-background {
  position: absolute;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  background: linear-gradient(180deg,
    #87CEEB 0%,
    #ADD8E6 30%,
    #B0E0E6 60%,
    #E0F4FF 100%);
  z-index: 0;
}

/* 彩虹条 */
.rainbow-bar {
  height: 8px;
  background: linear-gradient(90deg,
    #ff6b6b, #feca57, #48dbfb, #ff9ff3, #54a0ff);
  background-size: 200% 100%;
  animation: rainbowMove 3s linear infinite;
}

@keyframes rainbowMove {
  0% { background-position: 0% 50%; }
  100% { background-position: 200% 50%; }
}

/* 白云朵 */
.cloud {
  position: absolute;
  background: white;
  border-radius: 50%;
  box-shadow: 0 8px 20px rgba(255, 255, 255, 0.8);
  opacity: 0.9;
}

.cloud::before,
.cloud::after {
  content: '';
  position: absolute;
  background: white;
  border-radius: 50%;
}

.cloud-1 {
  width: 100px;
  height: 40px;
  top: 10%;
  left: -100px;
  animation: cloudFloat1 25s linear infinite;
}
.cloud-1::before { width: 50px; height: 50px; top: -25px; left: 15px; }
.cloud-1::after { width: 35px; height: 35px; top: -15px; left: 55px; }

.cloud-2 {
  width: 120px;
  height: 50px;
  top: 25%;
  left: -120px;
  animation: cloudFloat2 30s linear infinite;
  animation-delay: 5s;
}
.cloud-2::before { width: 60px; height: 60px; top: -30px; left: 20px; }
.cloud-2::after { width: 45px; height: 45px; top: -20px; left: 65px; }

.cloud-3 {
  width: 80px;
  height: 35px;
  top: 5%;
  left: -80px;
  animation: cloudFloat3 20s linear infinite;
  animation-delay: 10s;
}
.cloud-3::before { width: 40px; height: 40px; top: -20px; left: 10px; }
.cloud-3::after { width: 30px; height: 30px; top: -12px; left: 40px; }

.cloud-4 {
  width: 150px;
  height: 60px;
  top: 40%;
  left: -150px;
  animation: cloudFloat4 35s linear infinite;
  animation-delay: 3s;
}
.cloud-4::before { width: 70px; height: 70px; top: -35px; left: 25px; }
.cloud-4::after { width: 55px; height: 55px; top: -25px; left: 85px; }

.cloud-5 {
  width: 90px;
  height: 38px;
  top: 60%;
  left: -90px;
  animation: cloudFloat5 28s linear infinite;
  animation-delay: 8s;
}
.cloud-5::before { width: 45px; height: 45px; top: -22px; left: 12px; }
.cloud-5::after { width: 32px; height: 32px; top: -14px; left: 48px; }

.cloud-6 {
  width: 130px;
  height: 55px;
  top: 75%;
  left: -130px;
  animation: cloudFloat6 32s linear infinite;
  animation-delay: 12s;
}
.cloud-6::before { width: 65px; height: 65px; top: -32px; left: 22px; }
.cloud-6::after { width: 50px; height: 50px; top: -22px; left: 72px; }

@keyframes cloudFloat1 {
  0% { transform: translateX(0); }
  100% { transform: translateX(calc(100vw + 200px)); }
}
@keyframes cloudFloat2 {
  0% { transform: translateX(0); }
  100% { transform: translateX(calc(100vw + 240px)); }
}
@keyframes cloudFloat3 {
  0% { transform: translateX(0); }
  100% { transform: translateX(calc(100vw + 160px)); }
}
@keyframes cloudFloat4 {
  0% { transform: translateX(0); }
  100% { transform: translateX(calc(100vw + 300px)); }
}
@keyframes cloudFloat5 {
  0% { transform: translateX(0); }
  100% { transform: translateX(calc(100vw + 180px)); }
}
@keyframes cloudFloat6 {
  0% { transform: translateX(0); }
  100% { transform: translateX(calc(100vw + 260px)); }
}

/* 漂浮粒子 */
.particles {
  position: absolute;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  z-index: 1;
}

.particles span {
  position: absolute;
  width: 8px;
  height: 8px;
  background: radial-gradient(circle, rgba(255,255,255,0.8) 0%, transparent 70%);
  border-radius: 50%;
  animation: particleFloat 4s infinite ease-in-out;
  animation-delay: calc(var(--i) * 0.13s);
}

@keyframes particleFloat {
  0%, 100% {
    transform: translateY(0) translateX(0) scale(0);
    opacity: 0;
  }
  25% {
    opacity: 1;
    transform: translateY(-30px) translateX(10px) scale(1);
  }
  50% {
    transform: translateY(-60px) translateX(-10px) scale(0.8);
    opacity: 0.8;
  }
  75% {
    transform: translateY(-90px) translateX(5px) scale(0.5);
    opacity: 0.5;
  }
}

/* 卡片 */
.user-center-card {
  max-width: 480px;
  width: 100%;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(15px);
  border-radius: 24px;
  box-shadow:
    0 25px 60px rgba(135, 206, 235, 0.3),
    0 10px 30px rgba(0, 0, 0, 0.1);
  position: relative;
  z-index: 10;
  overflow: hidden;
}

.card-content {
  padding: 35px 30px;
  text-align: center;
}

/* 头像 */
.avatar-section {
  margin-bottom: 20px;
}

.cloud-avatar-bg {
  display: inline-block;
  padding: 15px;
  background: linear-gradient(135deg, #87CEEB 0%, #ADD8E6 50%, #B0E0E6 100%);
  border-radius: 50%;
  box-shadow:
    0 8px 30px rgba(135, 206, 235, 0.5),
    inset 0 -5px 20px rgba(135, 206, 235, 0.3);
  animation: avatarBounce 3s ease-in-out infinite;
}

@keyframes avatarBounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-8px); }
}

/* 标题 */
.title-section {
  margin-bottom: 25px;
}

.username {
  font-size: 30px;
  font-weight: bold;
  color: #2c3e50;
  margin: 0 0 10px 0;
  animation: fadeInDown 0.8s ease-out;
}

@keyframes fadeInDown {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.badge {
  display: inline-block;
  padding: 5px 15px;
  background: linear-gradient(135deg, #87CEEB, #ADD8E6);
  color: white;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 500;
  box-shadow: 0 3px 10px rgba(135, 206, 235, 0.4);
}

/* 信息卡片 */
.info-cards {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
  margin-bottom: 25px;
}

.info-card {
  display: flex;
  align-items: center;
  padding: 14px;
  background: linear-gradient(135deg, #f8fcff 0%, #e8f4ff 100%);
  border-radius: 16px;
  border: 1px solid rgba(135, 206, 235, 0.2);
  transition: all 0.3s ease;
  animation: fadeInUp 0.5s ease-out backwards;
}

.info-card:hover {
  transform: translateY(-3px) scale(1.02);
  box-shadow: 0 8px 25px rgba(135, 206, 235, 0.3);
  border-color: rgba(135, 206, 235, 0.5);
}

.info-card:nth-child(5) {
  grid-column: 1 / -1;
}

.info-icon {
  font-size: 22px;
  margin-right: 12px;
}

.info-text {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  text-align: left;
}

.info-label {
  font-size: 11px;
  color: #7f8c8d;
  margin-bottom: 2px;
}

.info-value {
  font-size: 13px;
  color: #2c3e50;
  font-weight: 500;
  max-width: 140px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 按钮 */
.button-group {
  display: flex;
  gap: 15px;
  justify-content: center;
}

.btn-edit, .btn-password {
  padding: 13px 28px;
  border-radius: 50px;
  font-weight: 600;
  font-size: 14px;
  transition: all 0.3s ease;
  border: none;
  letter-spacing: 1px;
}

.btn-edit {
  background: linear-gradient(135deg, #87CEEB 0%, #54a0ff 100%);
  color: white;
  box-shadow: 0 5px 20px rgba(135, 206, 235, 0.4);
}

.btn-edit:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 30px rgba(135, 206, 235, 0.5);
}

.btn-password {
  background: linear-gradient(135deg, #576574 0%, #222f3e 100%);
  color: white;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.2);
}

.btn-password:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
}

.btn-icon {
  margin-right: 6px;
}

/* 底部草地装饰 */
.grass-decoration {
  height: 30px;
  background: linear-gradient(180deg, #27ae60 0%, #2ecc71 50%, #82e0aa 100%);
  position: relative;
}

.grass-decoration::before {
  content: '';
  position: absolute;
  top: -10px;
  left: 0;
  width: 100%;
  height: 20px;
  background: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 20'%3E%3Cpath d='M0,20 Q10,0 20,20 Q30,5 40,20 Q50,0 60,20 Q70,5 80,20 Q90,0 100,20' fill='%232ecc71'/%3E%3C/svg%3E");
  background-size: 100px 20px;
  animation: grassWave 2s ease-in-out infinite;
}

@keyframes grassWave {
  0%, 100% { transform: scaleY(1); }
  50% { transform: scaleY(1.1); }
}
</style>

<style>
.input_box {
  width: 200px;
  margin-right: 20px;
}

.el-dialog .avatar-uploader .el-upload {
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
}

.el-dialog .avatar-uploader .el-upload:hover {
  border-color: #87CEEB;
}

.el-dialog .avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 100px;
  height: 100px;
  line-height: 100px;
  text-align: center;
}
</style>
