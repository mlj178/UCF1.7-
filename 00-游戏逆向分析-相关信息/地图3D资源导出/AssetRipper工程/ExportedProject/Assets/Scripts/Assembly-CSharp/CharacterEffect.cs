using System;
using System.Collections.Generic;
using UnityEngine;

public class CharacterEffect : MonoBehaviour
{
	[Serializable]
	public struct FxData
	{
		public Transform node;

		public Vector3 offset;

		public Vector3 euler;

		public GameObject fxPrefab;
	}

	[SerializeField]
	private FxData[] datas;

	[NonSerialized]
	public Player owner;

	private List<EffectObj> fxList;

	protected bool isFxEnable { get; private set; }

	public virtual void SetEffectState(bool active)
	{
	}

	protected EffectObj ApplyFxData(FxData data)
	{
		return null;
	}

	protected void RemoveEffect(EffectObj fx)
	{
	}
}
