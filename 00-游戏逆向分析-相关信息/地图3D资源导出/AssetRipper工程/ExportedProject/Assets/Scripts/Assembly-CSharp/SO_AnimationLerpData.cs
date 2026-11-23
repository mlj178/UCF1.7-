using System;
using RotaryHeart.Lib.SerializableDictionary;
using UnityEngine;

[CreateAssetMenu]
public class SO_AnimationLerpData : ScriptableObject
{
	[Serializable]
	internal class Dic : SerializableDictionaryBase<string, float>
	{
	}

	[SerializeField]
	private Dic dictionary;

	public float GetLerpTime(string animName)
	{
		return 0f;
	}
}
