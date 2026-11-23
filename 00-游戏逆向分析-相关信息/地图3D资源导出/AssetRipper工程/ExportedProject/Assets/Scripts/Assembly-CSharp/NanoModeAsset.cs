using RotaryHeart.Lib.SerializableDictionary;
using UnityEngine;

[CreateAssetMenu]
public class NanoModeAsset : ScriptableObject
{
	public int[] nanoGenerateCount;

	public string nanoTimerString;

	public string nanoAppearString;

	public GameObject nanoChangeFX;

	public GameObject respawnFX;

	public GameObject supplyBox;

	public RandomItem supplyBoxItems;

	public SerializableDictionaryBase<string, Texture> markDic;

	public Texture GetMark(string markName)
	{
		return null;
	}
}
