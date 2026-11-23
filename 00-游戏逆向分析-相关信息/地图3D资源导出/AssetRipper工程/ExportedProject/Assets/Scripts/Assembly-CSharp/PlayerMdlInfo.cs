using System.Collections.Generic;
using System.Runtime.CompilerServices;
using CustomEvent;
using UnityEngine;
using UnityEngine.Rendering;

public class PlayerMdlInfo
{
	internal struct MatData
	{
		public Material mat;

		public bool isTransparent;
	}

	public enum FxType
	{
		None = 0,
		HumanRespawn = 1,
		NanoInLowHp = 2,
		Absorbed = 3
	}

	private SubscribeableProperty<Color> pvColor;

	private SubscribeableProperty<Color> cvColor;

	private List<MatData> pvMatList;

	private List<MatData> cvMatList;

	private static readonly Color AbsorbedColor;

	public FxType fxType;

	[CompilerGenerated]
	private Ref2Float m_Getter_Alpha;

	private List<Renderer> cvRenderers;

	public float cvAlpha { get; private set; }

	public event Ref2Float Getter_Alpha
	{
		[CompilerGenerated]
		add
		{
		}
		[CompilerGenerated]
		remove
		{
		}
	}

	public void AddModel(Model mdl)
	{
	}

	public void RemoveModel(Model mdl)
	{
	}

	private void AddMat(Material mat, List<MatData> list, Color color)
	{
	}

	private void RemoveMat(Material mat, List<MatData> list)
	{
	}

	private void UpdateListColor(List<MatData> list, Color oldColor, Color newColor)
	{
	}

	public void Update()
	{
	}

	private ShadowCastingMode GetShadowCastingMode()
	{
		return ShadowCastingMode.Off;
	}

	private void UpdateShadowCaster()
	{
	}
}
