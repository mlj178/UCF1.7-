using System;
using System.Collections.Generic;
using RotaryHeart.Lib.SerializableDictionary;
using UnityEngine;

[CreateAssetMenu]
public class NanoModeBasicAsset : ScriptableObject
{
	[Serializable]
	public struct NameIntArray
	{
		public string name;

		public int[] datas;
	}

	public AudioClip[] SND_Timer;

	public AudioClip[] SND_RoundResult;

	public AudioClip SND_SupplyBoxArrive;

	public AudioClip[] SND_HpRecover;

	public List<NameIntArray> wpnList;

	public Texture2D mark_Absorb;

	public Texture2D mark_DefenseNano;

	public Texture2D mark_InfectFailed;

	public Texture2D[] Mark_NanoMultiKill;

	[SerializeField]
	private GameObject[] fx_shield;

	public GameObject Gauge_Absorb;

	[SerializeField]
	private SerializableDictionaryBase<string, GameObject> nanoRoleChangeFxDic;

	public GameObject RadarIcon_Hero;

	public GameObject NanoRoleSign;

	public SerializableDictionaryBase<string, Sprite> roleSignDic;

	[SerializeField]
	public GameObject[] skillBtns;

	[SerializeField]
	public GameObject[] screenEffects;

	public void GiveWeapon(Player player)
	{
	}

	public void TrySetHealth(Player player)
	{
	}

	public bool TryGetChangeFx(NanoRole role, out GameObject result)
	{
		result = null;
		return false;
	}

	public GameObject GetTerminatorShield(NanoRole nanoRole)
	{
		return null;
	}

	public GameObject GetSkillBtn(NanoRole nanoRole)
	{
		return null;
	}

	public GameObject GetScreenEffect(NanoRole nanoRole)
	{
		return null;
	}
}
