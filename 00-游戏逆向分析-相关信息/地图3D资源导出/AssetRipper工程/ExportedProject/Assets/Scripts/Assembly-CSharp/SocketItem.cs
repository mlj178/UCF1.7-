using System;
using UnityEngine;

public class SocketItem : MonoBehaviour
{
	[Serializable]
	public enum ItemType
	{
		HeadSet = 0,
		EyeWear = 1,
		Backpack = 2,
		Thigh = 3,
		Waist = 4,
		Shoulder = 5
	}

	public ItemType itemType;

	private static readonly Vector3 itemEuler;

	public virtual void BindOnCharacter(CharacterModel characterModel)
	{
	}
}
