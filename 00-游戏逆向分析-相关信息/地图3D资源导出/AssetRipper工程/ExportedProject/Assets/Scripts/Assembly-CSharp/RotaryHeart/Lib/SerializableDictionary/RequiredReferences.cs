using UnityEngine;

namespace RotaryHeart.Lib.SerializableDictionary
{
	public class RequiredReferences : ScriptableObject
	{
		[SerializeField]
		private GameObject _gameObject;

		[SerializeField]
		private Material _material;

		[SerializeField]
		private AudioClip _audioClip;
	}
}
