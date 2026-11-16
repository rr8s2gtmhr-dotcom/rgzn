<template>
	<el-dialog v-model="visible" :title="initial.id ? '修改用户' : '新增用户'" width="520px" destroy-on-close>
		<el-form ref="formRef" :model="form" :rules="rules" label-width="90px" size="default">
			<el-form-item label="用户名" prop="userName">
				<el-input v-model="form.userName" placeholder="请输入用户名" clearable />
			</el-form-item>
			<el-form-item label="姓名" prop="realName">
				<el-input v-model="form.realName" placeholder="请输入姓名" clearable />
			</el-form-item>
			<el-form-item label="手机号" prop="phone">
				<el-input v-model="form.phone" placeholder="请输入手机号" clearable />
			</el-form-item>
			<el-form-item label="所属单位">
				<el-select v-model="form.unitId" placeholder="请选择单位" clearable style="width: 100%">
					<el-option v-for="unit in units" :key="unit.id" :label="unit.deptName" :value="unit.id" />
				</el-select>
			</el-form-item>
			<el-form-item label="关联角色">
				<el-select v-model="form.roleIds" multiple placeholder="请选择角色" style="width: 100%">
					<el-option v-for="role in roles" :key="role.id" :label="role.roleName" :value="role.id" />
				</el-select>
			</el-form-item>
			<el-form-item label="用户状态">
				<el-switch v-model="form.status" />
			</el-form-item>
		</el-form>
		<template #footer>
			<el-button @click="visible = false">取 消</el-button>
			<el-button type="primary" @click="onSubmit">确 定</el-button>
		</template>
	</el-dialog>
</template>

<script setup lang="ts" name="systemUserDialog">
import { computed, reactive, ref, watch } from 'vue';
import type { FormInstance } from 'element-plus';

const props = defineProps({
	modelValue: { type: Boolean, default: false },
	initial: { type: Object, default: () => ({}) },
	units: { type: Array as () => EmptyObjectType[], default: () => [] },
	roles: { type: Array as () => EmptyObjectType[], default: () => [] },
});
const emit = defineEmits(['update:modelValue', 'submit']);

const formRef = ref<FormInstance>();
const form = reactive<EmptyObjectType>({ userName: '', realName: '', phone: '', unitId: null, roleIds: [], status: true });

const visible = computed({
	get: () => props.modelValue,
	set: (value: boolean) => emit('update:modelValue', value),
});
const rules = {
	userName: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
	realName: [{ required: true, message: '请输入姓名', trigger: 'blur' }],
	phone: [{ required: true, message: '请输入手机号', trigger: 'blur' }],
};

watch(
	() => props.modelValue,
	(value) => {
		if (!value) return;
		Object.assign(form, {
			id: props.initial.id,
			userName: props.initial.userName || '',
			realName: props.initial.realName || '',
			phone: props.initial.phone || '',
			unitId: props.initial.unitId || null,
			roleIds: props.initial.roleIds || [],
			status: props.initial.status ?? true,
		});
	}
);

const onSubmit = () => {
	formRef.value?.validate((valid: boolean) => {
		if (!valid) return;
		emit('submit', { ...form });
		visible.value = false;
	});
};
</script>
