<template>
	<el-dialog v-model="visible" :title="title" width="600px" destroy-on-close>
		<el-form ref="formRef" :model="form" :rules="rules" size="default" label-width="100px">
			<el-form-item v-for="field in fields" :key="field.key" :label="field.label" :prop="field.key">
				<el-input
					v-if="!field.type || field.type === 'input'"
					v-model="form[field.key]"
					:placeholder="field.placeholder || `请输入${field.label}`"
					clearable
				/>
				<el-input
					v-else-if="field.type === 'textarea'"
					v-model="form[field.key]"
					type="textarea"
					:rows="3"
					:placeholder="field.placeholder || `请输入${field.label}`"
				/>
				<el-date-picker
					v-else-if="field.type === 'date'"
					v-model="form[field.key]"
					type="date"
					value-format="YYYY-MM-DD"
					:placeholder="field.placeholder || `请选择${field.label}`"
					style="width: 100%"
				/>
				<el-select
					v-else-if="field.type === 'select'"
					v-model="form[field.key]"
					:placeholder="field.placeholder || `请选择${field.label}`"
					clearable
					style="width: 100%"
				>
					<el-option v-for="option in field.options || []" :key="option.value" :label="option.label" :value="option.value" />
				</el-select>
				<el-switch v-else-if="field.type === 'switch'" v-model="form[field.key]" />
				<el-input-number v-else-if="field.type === 'number'" v-model="form[field.key]" :min="0" controls-position="right" style="width: 100%" />
			</el-form-item>
		</el-form>
		<template #footer>
			<el-button @click="visible = false">取 消</el-button>
			<el-button type="primary" @click="onSubmit">确 定</el-button>
		</template>
	</el-dialog>
</template>

<script setup lang="ts" name="crudDialog">
import { computed, nextTick, reactive, ref, watch } from 'vue';
import type { FormInstance } from 'element-plus';

const props = defineProps({
	modelValue: { type: Boolean, default: false },
	title: { type: String, default: '' },
	fields: { type: Array as () => CrudField[], default: () => [] },
	initial: { type: Object, default: () => ({}) },
});

const emit = defineEmits(['update:modelValue', 'submit']);

const formRef = ref<FormInstance>();
const form = reactive<EmptyObjectType>({});

const visible = computed({
	get: () => props.modelValue,
	set: (value: boolean) => emit('update:modelValue', value),
});

const rules = computed(() => {
	const result: EmptyObjectType = {};
	props.fields.forEach((field) => {
		if (field.required) result[field.key] = [{ required: true, message: `请输入${field.label}`, trigger: 'blur' }];
	});
	return result;
});

watch(
	() => props.modelValue,
	(value) => {
		if (!value) return;
		Object.keys(form).forEach((key) => delete form[key]);
		Object.assign(form, props.initial || {});
		props.fields.forEach((field) => {
			if (form[field.key] === undefined) form[field.key] = field.type === 'switch' ? false : '';
		});
		nextTick(() => formRef.value?.clearValidate());
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
