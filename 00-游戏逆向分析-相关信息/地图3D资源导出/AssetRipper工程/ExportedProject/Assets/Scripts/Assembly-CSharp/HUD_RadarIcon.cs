using UnityEngine;
using UnityEngine.UI;

public class HUD_RadarIcon : RecyclableObject
{
	[SerializeField]
	protected RectTransform rectTransform;

	[SerializeField]
	protected Image image;

	protected Transform bindTransform;

	protected Vector3 delta3dPos;

	public bool rotateAtEdge;

	protected bool atEdge { get; private set; }

	protected Player focusPlayer => null;

	public bool maskable
	{
		get
		{
			return false;
		}
		set
		{
		}
	}

	protected virtual void Update()
	{
	}

	private void UpdateTransform()
	{
	}

	public virtual bool IsVisible()
	{
		return false;
	}

	public void SetSprite(Sprite sprite)
	{
	}

	public void Bind(Transform bind)
	{
	}

	protected override void Work()
	{
	}

	public override void Recycle(bool roundRecycle)
	{
	}
}
