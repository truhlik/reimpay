export default function updateField(instance, updateObject) {
  instance[updateObject.field] = updateObject.value;
}
