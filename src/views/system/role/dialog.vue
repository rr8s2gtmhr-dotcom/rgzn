<template>
	<el-dialog v-model="visible" :title="initial.id ? '修改角色' : '新增角色'" width="680px" destroy-on-close>
		<el-form ref="formRef" :model="form" :rules="rules" label-width="100px" size="default">
			<el-form-item label="角色名称" prop="roleName">
				<el-input v-model="form.roleName" placeholder="请输入角色名称" clearable />
			</el-form-item>
			<el-form-item label="数据范围" prop="dataScope">
				<el-select v-model="form.dataScope" placeholder="请选择数据范围" style="width: 100%">
					<el-option label="全部" value="全部" />
					<el-option label="本单位" value="本单位" />
					<el-option label="本部门" value="本部门" />
					<el-option label="仅本人" value="仅本人" />
				</el-select>
			</el-form-item>
			<el-form-item label="菜单权限">
				<el-tree
					ref="treeRef"
					:data="treeData"
					node-key="path"
					show-checkbox
					default-expand-all
					:props="{ label: 'label', children: 'children' }"
				/>
			</el-form-item>
			<el-form-item label="按钮权限">
				<el-checkbox-group v-model="form.btnPermissions">
					<el-checkbox v-for="item in buttonPermissions" :key="item" :label="item" />
				</el-checkbox-group>
			</el-form-item>
		</el-form>
		<template #footer>
			<el-button @click="visible = false">取 消</el-button>
			<el-button type="primary" @click="onSubmit">确 定</el-button>
		</template>
	</el-dialog>
</template>

<script setup lang="ts" name="systemRoleDialog">
import { computed, nextTick, reactive, ref, watch } from 'vue';
import type { FormInstance } from 'element-plus';
import { i18n } from '/@/i18n/index';
import type { LocalMenu } from '/@/types/api';

const props = defineProps({
	modelValue: { type: Boolean, default: false },
	initial: { type: Object, default: () => ({}) },
	menus: { type: Array as () => LocalMenu[], default: () => [] },
});
const emit = defineEmits(['update:modelValue', 'submit']);

const buttonPermissions = ['btn.add', 'btn.edit', 'btn.del', 'btn.link', 'btn.export'];
const formRef = ref<FormInstance>();
const treeRef = ref();
const form = reactive<EmptyObjectType>({ roleName: '', dataScope: '全部', menuPaths: [], btnPermissions: [] });

const visible = computed({
	get: () => props.modelValue,
	set: (value: boolean) => emit('update:modelValue', value),
});
const rules = {
	roleName: [{ required: true, message: '请输入角色名称', trigger: 'blur' }],
	dataScope: [{ required: true, message: '请选择数据范围', trigger: 'change' }],
};
const treeData = computed(() => {
	const build = (pid: number | null): any[] =>
		props.menus
			.filter((menu) => menu.pid === pid)
			.map((menu) => ({
				path: menu.path,
				label: i18n.global.t(menu.meta.title),
				children: build(menu.id),
			}));
	return build(null);
});

watch(
	() => props.modelValue,
	(value) => {
		if (!value) return;
		Object.assign(form, {
			id: props.initial.id,
			code: props.initial.code || `role_${Date.now()}`,
			roleName: props.initial.roleName || '',
			dataScope: props.initial.dataScope || '全部',
			menuPaths: props.initial.menuPaths || [],
			btnPermissions: props.initial.btnPermissions || [],
		});
		nextTick(() => treeRef.value?.setCheckedKeys(form.menuPaths));
	}
);

const onSubmit = () => {
	formRef.value?.validate((valid: boolean) => {
		if (!valid) return;
		emit('submit', {
			...form,
			menuPaths: treeRef.value?.getCheckedKeys() || [],
		});
		visible.value = false;
	});
};
</script>
