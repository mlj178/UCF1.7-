using System.Collections.Generic;
using UnityEngine;

[CreateAssetMenu]
public class CharacterAsset : ScriptableObject
{
	public List<GameObject> characterList;

	public List<GameObject> socketItems;

	public GameObject GetCharacterPrefab(string name)
	{
		return null;
	}

	public GameObject GetSocketItemPrefab(string name)
	{
		return null;
	}
}
